""" process_manager.pyのテスト """
import pytest
from unittest.mock import patch
import time
from multiprocessing import Process, Pipe
from multiprocessing.connection import Connection
from yt_diffuser.main import process_manager

def proc(shared_conn:Connection, parent_conn:Connection):
    """ テスト用プロセス
    """
    while True:
        time.sleep(1)


class TestCleanup:
    """ describe: cleanup クリーンアップ処理 """
    
    @pytest.mark.dependency()
    def test_cleanup(self):
        """ it: 登録されている全プロセスを終了し、クリーンアップする。 """

        process_manager._conns["parent"], process_manager._conns["child"] = Pipe()
        process_manager._conns["shared1"], process_manager._conns["shared2"] = Pipe()

        p1 = Process(target=proc, args=(process_manager._conns["shared1"], process_manager._conns["child"]))
        p2 = Process(target=proc, args=(process_manager._conns["shared2"], process_manager._conns["child"]))

        process_manager._procs["web"] = p1
        process_manager._procs["processing"] = p2
        process_manager._targets["web"] = proc
        process_manager._targets["processing"] = proc

        p1.start()
        p2.start()

        process_manager.cleanup()

        assert process_manager._targets["web"] == None
        assert process_manager._targets["processing"] == None
        assert process_manager._procs["web"] == None
        assert process_manager._procs["processing"] == None
        assert p1.is_alive() == False
        assert p2.is_alive() == False
        assert process_manager._conns["parent"] == None
        assert process_manager._conns["child"] == None
        assert process_manager._conns["shared1"] == None
        assert process_manager._conns["shared2"] == None

@pytest.mark.dependency(depends=["TestCleanup::test_cleanup"])
class TestInit():
    """ describe: init 初期化処理 """

    def test_init(self):
        """ it: プロセスマネージャーを初期化する。 """

        assert process_manager._procs["web"] == None
        assert process_manager._procs["processing"] == None

        process_manager.init(proc, proc)

        assert process_manager._targets["web"] == proc
        assert process_manager._targets["processing"] == proc
        assert type(process_manager._procs["web"]) == Process
        assert type(process_manager._procs["processing"]) == Process
        assert type(process_manager._conns["parent"]) == Connection

    def test_init_cleanup(self):
        """ it: 処理開始時にはクリーンアップを行う。 """

        # モック化するので一度クリーンアップしておく
        process_manager.cleanup()

        with patch('yt_diffuser.main.process_manager.cleanup') as mock_cleanup:
            process_manager.init(proc, proc)

        mock_cleanup.assert_called_once()

class TestSignalHandler:
    """ describe: signal_handler 終了シグナルハンドラ """

    def test_signal_handler(self):
        """ it: 終了シグナルを受け取った場合にcleanupを呼び出し、プロセスを終了する。基本的にsignal.signalで登録して使う。 """

        with patch('yt_diffuser.main.process_manager.cleanup') as mock_cleanup:

            with pytest.raises(SystemExit):
                process_manager.signal_handler(0, None)

        mock_cleanup.assert_called_once()

@pytest.mark.dependency(depends=["TestInit::test_init"])
class TestStartAll:
    """ describe: start_all プロセス開始 """

    def test_start_all_no_init(self):
        """ it: initが呼ばれていない場合は例外を投げる。 """
        process_manager.cleanup()
        with pytest.raises(Exception):
            process_manager.start_all()

    def test_start_all(self, monkeypatch):
        """ it: サブプロセスが起動され、サブプロセスから終了要求があると終了する。"""

        def web_main(shared_conn:Connection, parent_conn:Connection):
            parent_conn.send("exit")

        def processing_main(shared_conn:Connection, parent_conn:Connection):
            pass

        process_manager.init(web_main, processing_main)
        assert process_manager.start_all() is None
    
    def test_process_main2(self, monkeypatch):
        """ it: 終了要求はどちらからでも出せる。データ処理プロセス側から終わらせるパターンはない気もするが…。"""

        def web_main(shared_conn:Connection, parent_conn:Connection):
            pass

        def processing_main(shared_conn:Connection, parent_conn:Connection):
            parent_conn.send("exit")

        process_manager.init(web_main, processing_main)
        assert process_manager.start_all() is None
 
    def test_conn(self, monkeypatch):
        """ it: サブプロセス同士はConnectionを使って通信できる。"""

        # テストの説明：processing_mainはweb_mainからメッセージを受け取るまでメッセージを送らず、web_mainはprocessing_mainからメッセージを受け取るまでメインに終了要求をしない。
        # そのため、メインがエラーなく終了した場合、サブプロセス同士が通信できていることが確認できる。
        def web_main(shared_conn:Connection, parent_conn:Connection):
            shared_conn.send("hi")
            msg = shared_conn.recv()
            if msg == "hello":
                parent_conn.send("exit")
        
        def processing_main(shared_conn:Connection, parent_conn:Connection):
            msg = shared_conn.recv()
            if msg == "hi":
                shared_conn.send("hello")
        
        process_manager.init(web_main, processing_main)
        assert process_manager.start_all() is None

        process_manager.init(processing_main, web_main)
        assert process_manager.start_all() is None

    def test_restart(self, monkeypatch):
        """ it: サブプロセスがメインプロセス終了要求なしに終了した場合、メインプロセスはサブプロセスを再起動する。"""

        # テスト説明：web_mainは起動時にprocessing_mainにメッセージを送って終了する。processing_mainはメッセージを2回受け取ると終了要求を出す。
        # これによりweb_mainが2回起動している確認ができる。
        def web_main(shared_conn:Connection, parent_conn:Connection):
            shared_conn.send("hi")
            return
        
        def processing_main(shared_conn:Connection, parent_conn:Connection):
            msg = shared_conn.recv()
            if msg == "hi":
                shared_conn.send("hello")
            msg = shared_conn.recv()
            if msg == "hi":
                parent_conn.send("exit")
 
        process_manager.init(web_main, processing_main)
        assert process_manager.start_all() is None

        process_manager.init(processing_main, web_main)
        assert process_manager.start_all() is None
