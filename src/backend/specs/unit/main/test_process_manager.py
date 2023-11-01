""" process_manager.pyのテスト """
import pytest
from unittest.mock import patch
import time
from multiprocessing import Process, Pipe
from multiprocessing.connection import Connection
from yt_diffuser.main import process_manager

class TestStopAll:
    """ describe: stop_all 停止処理 """
    
    @pytest.mark.dependency
    def test_stop_all(self):
        """ it: 登録されている全プロセスを終了し、クリーンアップする。 """

        process_manager._parent_conn, process_manager._child_conn = Pipe()

        process_manager._processes["Web"]["shared_conn"], process_manager._processes["Worker"]["shared_conn"] = Pipe()

        ps = []
        for key, p in process_manager._processes.items():
            ps.append(Process(target=dummy_proc, args=(p["shared_conn"], process_manager._child_conn)))
            p["process"] = ps[-1]
            p["process"].start() 

        process_manager.stop_all()

        for key, p in process_manager._processes.items():
            assert p["process"] == None
            assert p["shared_conn"] == None
        
        for p in ps:
            assert p.is_alive() == False

class TestSignalHandler:
    """ describe: signal_handler 終了シグナルハンドラ """

    def test_signal_handler(self):
        """ it: 終了シグナルを受け取った場合にstop_allを呼び出し、プロセスを終了する。基本的にsignal.signalで登録して使う。 
        """

        with patch('yt_diffuser.main.process_manager.stop_all') as mock_stop_all:

            with pytest.raises(SystemExit):
                process_manager.signal_handler(0, None)

        mock_stop_all.assert_called_once()

class TestStartAll:
    """ describe: start_all プロセス開始 """

    @pytest.mark.dependency
    def test_start_all(self, monkeypatch):
        """ it: サブプロセスが起動され、サブプロセスから終了要求があると終了する。
            終了要求はどちらからでも出せる。
            ワーカープロセス側から終了要求を出すパターンは実態としては存在しないが、処理の簡素化のために実装している。
        """

        assert process_manager.start_all(web_procedure=dummy_proc_exit, worker_procedure=dummy_proc) is None
        assert process_manager.start_all(web_procedure=dummy_proc, worker_procedure=dummy_proc_exit) is None

    def test_init(self):
        """ it: プロセス開始時に初期化処理を行う。
            プロセス終了時に子プロセスを終了するためのシグナルハンドラ等を登録する。
        """

        with patch('yt_diffuser.main.process_manager.atexit.register') as mock_atexit_register ,\
            patch('yt_diffuser.main.process_manager.signal.signal') as mock_signal:

            process_manager.start_all(dummy_proc_exit, dummy_proc_exit)
        
        assert mock_atexit_register.call_count == 1
        assert mock_signal.call_count == 2
 
    def test_conn(self, monkeypatch):
        """ it: サブプロセス同士はConnectionを使って通信できる。
        """

        # テストの説明：
        # dummy_proc_conn_send_recv_exit は dummy_proc_conn_recv にメッセージを送る。
        # dummy_proc_conn_recv はメッセージを受け取ると、dummy_proc_conn_send_recv_exit にメッセージを返す。
        # dummy_proc_conn_send_recv_exit はメッセージを受け取ると終了要求を出す。
        # そのため、メインがエラーなく終了した場合、サブプロセス同士が通信できていることが確認できる。
        assert process_manager.start_all(dummy_proc_conn_send_recv_exit, dummy_proc_conn_recv) is None
        assert process_manager.start_all(dummy_proc_conn_recv, dummy_proc_conn_send_recv_exit) is None

    def test_restart(self, monkeypatch):
        """ it: サブプロセスがメインプロセスへの終了要求をせずに終了した場合、メインプロセスはサブプロセスを再起動する。
        """

        # テストの説明：
        # dummy_proc_conn_send_stop は dummy_proc_conn_recv にメッセージを送り、そのまま終了する。
        # dummy_proc_conn_recv_twice_exit はメッセージを2回受け取ると終了要求を出す。
        # これにより、メインがエラーなく終了した場合、dummy_proc_conn_recv_twice_exit が2回メッセージを受け取った＝ dummy_proc_conn_send_stop が2回起動したことが確認できる。
        assert process_manager.start_all(dummy_proc_conn_send_stop, dummy_proc_conn_recv_twice_exit) is None
        assert process_manager.start_all(dummy_proc_conn_recv_twice_exit, dummy_proc_conn_send_stop) is None

@pytest.mark.dependency(depends=["TestStartAll::test_start_all"])
class TestQuit:
    """ test: プロセス終了処理の確認 """

    def test_quit(self):
        """ it: 終了要求を受け取ると、子プロセスを終了し、メインプロセスを終了する。 """

        p = Process(target=process_manager.start_all, args=(dummy_proc, dummy_proc))
        p.start()

        time.sleep(1)
        # エラーなく終了できればOK
        p.terminate()
        p.join()

        assert p.exitcode == 0

def dummy_proc(shared_conn:Connection, parent_conn:Connection):
    """ ダミープロシージャ 無限ループ
    """
    while True:
        time.sleep(1)

def dummy_proc_exit(shared_conn:Connection, parent_conn:Connection):
    """ ダミープロシージャ 終了要求
    """
    parent_conn.send("exit")

def dummy_proc_conn_send_recv_exit(shared_conn:Connection, parent_conn:Connection):
    """ ダミープロシージャ メッセージ送信後、返信を受け取ったら終了要求
    """
    shared_conn.send("hi")

    if shared_conn.poll(timeout=5) == False:
        raise Exception("timeout")
    
    msg = shared_conn.recv()
    if msg == "hello":
        parent_conn.send("exit")

def dummy_proc_conn_recv(shared_conn:Connection, parent_conn:Connection):
    """ ダミープロシージャ メッセージ受信
    """    
    if shared_conn.poll(timeout=5) == False:
        raise Exception("timeout")

    msg = shared_conn.recv()
    if msg == "hi":
        print("send hello")
        shared_conn.send("hello")
    while True:
        time.sleep(1)

def dummy_proc_conn_send_stop (shared_conn:Connection, parent_conn:Connection):
    """ ダミープロシージャ メッセージ送信後、プロセス終了
    """
    shared_conn.send("hi")
    return

def dummy_proc_conn_recv_twice_exit(shared_conn:Connection, parent_conn:Connection):
    """ ダミープロシージャ メッセージを2回受信したら終了要求
    """
    if shared_conn.poll(timeout=5) == False:
        raise Exception("timeout")

    msg = shared_conn.recv()
    if msg == "hi":
        shared_conn.send("hello")

    if shared_conn.poll(timeout=5) == False:
        raise Exception("timeout")

    msg = shared_conn.recv()
    if msg == "hi":
        parent_conn.send("exit")