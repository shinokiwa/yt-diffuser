""" main.pyのテスト """
from multiprocessing.connection import Connection
from yt_diffuser.main.main import process

class TestProcess:
    """ describe: メインプロセス用メインルーチン"""

    def test_process_main(self, monkeypatch):
        """ it: サブプロセスが起動され、サブプロセスから終了要求があると終了する。"""

        def web_main(shared_conn:Connection, parent_conn:Connection):
            parent_conn.send("exit")

        def processing_main(shared_conn:Connection, parent_conn:Connection):
            pass

        assert process(web_main=web_main, processing_main=processing_main) is None
    
    def test_process_main2(self, monkeypatch):
        """ it: 終了要求はどちらからでも出せる。データ処理プロセス側から終わらせるパターンはない気もするが…。"""

        def web_main(shared_conn:Connection, parent_conn:Connection):
            pass

        def processing_main(shared_conn:Connection, parent_conn:Connection):
            parent_conn.send("exit")

        assert process(web_main=web_main, processing_main=processing_main) is None
 
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
        
        assert process(web_main=web_main, processing_main=processing_main) is None
        assert process(web_main=processing_main, processing_main=web_main) is None

    def test_restart(self, monkeypatch, caplog):
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
        
        # ついでにログ出力も確認する。

        assert process(web_main=web_main, processing_main=processing_main) is None
        assert 'WARNING' in caplog.text
        assert 'Web process is dead. Restarting...' in caplog.text

        assert process(web_main=processing_main, processing_main=web_main) is None
        assert 'WARNING' in caplog.text
        assert 'Processing process is dead. Restarting...' in caplog.text

