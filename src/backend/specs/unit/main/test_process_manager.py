""" process_manager.pyのテスト """
import pytest
from unittest.mock import patch
import time

from multiprocessing import Process, Pipe
from multiprocessing.connection import Connection
from multiprocessing.context import SpawnProcess

from yt_diffuser.main import process_manager

class TestStopAll:
    """ describe: stop_all 停止処理 """
    
    @pytest.mark.dependency
    def test_stop_all(self):
        """ it: 登録されている全プロセスを終了し、クリーンアップする。 """

        process_manager._processes["Web"]["shared_conn"], process_manager._processes["Worker"]["shared_conn"] = Pipe()

        ps = []
        for key, p in process_manager._processes.items():
            ps.append(Process(target=dummy_proc_loop, args=[p["shared_conn"]]))
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

class TestStartProcesses:
    """ describe: start_processes サブプロセス初期化 """

    def test_default (self, mocker):
        """ it: サブプロセスを初期化する。
        """
        with patch('yt_diffuser.main.process_manager._processes', {
            "Web": {"process": None, "shared_conn": None, "target": None}, "Worker": {"process": None, "shared_conn": None, "target": None}
        }) as _processes:

            process_manager.start_processes(dummy_proc, dummy_proc)

            assert _processes["Web"]["target"] == dummy_proc
            assert _processes["Worker"]["target"] == dummy_proc

            assert type(_processes["Web"]["shared_conn"]) == Connection
            assert type(_processes["Worker"]["shared_conn"]) == Connection

            assert type(_processes["Web"]["process"] ) == SpawnProcess
            assert type(_processes["Worker"]["process"] ) == SpawnProcess
 
    def test_conn(self, monkeypatch):
        """ it: サブプロセス同士はConnectionを使って通信できる。
        """

        with patch('yt_diffuser.main.process_manager._processes', {
            "Web": {"process": None, "shared_conn": None, "target": None}, "Worker": {"process": None, "shared_conn": None, "target": None}
        }) as _processes:

            process_manager.start_processes(dummy_proc_send, dummy_proc_recv)
            assert type( _processes["Worker"]["process"] ) == SpawnProcess
            assert _processes["Web"]["shared_conn"].recv() == "dummy reply"

            process_manager.start_processes(dummy_proc_recv, dummy_proc_send)
            assert type( _processes["Web"]["process"] ) == SpawnProcess
            assert _processes["Worker"]["shared_conn"].recv() == "dummy reply"


class TestCheckProcesses:
    """ describe: check_processes プロセス監視 """

    def test_default (self, mocker):
        """ it: プロセスが停止していた場合、再起動する。
        """
        shared_conn1, shared_conn2 = Pipe()

        with patch('yt_diffuser.main.process_manager._processes', {
            "Web": {"process": None, "shared_conn": shared_conn1, "target": dummy_proc_loop},
            "Worker": {"process": None, "shared_conn": shared_conn2, "target": dummy_proc_loop}
        }) as _processes:

            process_manager.check_processes()

            assert type(_processes["Web"]["process"] ) == SpawnProcess
            assert type(_processes["Worker"]["process"] ) == SpawnProcess
            assert _processes["Web"]["process"].is_alive() == True
            assert _processes["Worker"]["process"].is_alive() == True


            _processes["Web"]["process"].kill()
            _processes["Web"]["process"].join()
            assert _processes["Web"]["process"].is_alive() == False

            process_manager.check_processes()

            assert type(_processes["Web"]["process"] ) == SpawnProcess
            assert _processes["Web"]["process"].is_alive() == True

class TestStartLoop:
    """ describe: start_loop プロセス起動と監視開始 """

    def test_start_all(self, mocker):
        """ it: サブプロセスが起動され、監視が開始される。
        """

        mock_atexit_unregister = mocker.patch('yt_diffuser.main.process_manager.atexit.unregister')
        mock_atexit_register = mocker.patch('yt_diffuser.main.process_manager.atexit.register')
        mock_signal = mocker.patch('yt_diffuser.main.process_manager.signal.signal')
        mock_start_processes = mocker.patch('yt_diffuser.main.process_manager.start_processes')
        mock_check_processes = mocker.patch('yt_diffuser.main.process_manager.check_processes')
        mock_loop_listener = mocker.patch('yt_diffuser.main.process_manager.loop_listener')

        process_manager.start_loop(dummy_proc, dummy_proc)

        assert mock_atexit_unregister.call_count == 1
        assert mock_atexit_register.call_count == 1
        assert mock_signal.call_count == 2
        assert mock_start_processes.call_count == 1
        assert mock_loop_listener.call_count == 1
        assert mock_loop_listener.call_args[1]["loop_callback"] == mock_check_processes

def dummy_proc(shared_conn:Connection):
    """ ダミープロシージャ 即終了
    """
    return

def dummy_proc_loop(shared_conn:Connection):
    """ ダミープロシージャ 無限ループ
    """
    while True:
        time.sleep(1)

def dummy_proc_send(shared_conn:Connection):
    """ ダミープロシージャ メッセージ送信
    """
    shared_conn.send("dummy")

def dummy_proc_recv(shared_conn:Connection):
    """ ダミープロシージャ メッセージ受信
    """
    shared_conn.recv()
    shared_conn.send("dummy reply")