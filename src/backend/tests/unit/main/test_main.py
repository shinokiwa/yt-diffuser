""" main.pyのテスト
"""
import unittest
from multiprocessing.connection import Connection
from yt_diffuser.main.main import process

class TestMain(unittest.TestCase):
    """ main.pyのテスト
    """
    def test_process(self):
        """ processのテスト
        """

        # サブプロセスが起動され、サブプロセスから終了要求があると終了する。
        def web_main(shared_conn:Connection, parent_conn:Connection):
            parent_conn.send("exit")

        def processing_main(shared_conn:Connection, parent_conn:Connection):
            pass

        self.assertIsNone(process(web_main=web_main, processing_main=processing_main))

        # 終了要求はどちらからでも出せる。データ処理プロセス側から終わらせるパターンはない気もするが…。
        self.assertIsNone(process(web_main=processing_main, processing_main=web_main))

        # サブプロセス同士は通信できる
        ## テスト説明：processing_mainはweb_mainからメッセージを受け取るまでメッセージを送らず、web_mainはprocessing_mainからメッセージを受け取るまでメインに終了要求をしない。
        def web_main(shared_conn:Connection, parent_conn:Connection):
            shared_conn.send("hi")
            msg = shared_conn.recv()
            if msg == "hello":
                parent_conn.send("exit")

        def processing_main(shared_conn:Connection, parent_conn:Connection):
            msg = shared_conn.recv()
            if msg == "hi":
                shared_conn.send("hello")

        self.assertIsNone(process(web_main=web_main, processing_main=processing_main))
        self.assertIsNone(process(web_main=processing_main, processing_main=web_main))

        # サブプロセスがメインプロセス終了要求なしに終了した場合、メインプロセスはサブプロセスを再起動する。
        ## テスト説明：web_mainは起動時にprocessing_mainにメッセージを送って終了する。processing_mainはメッセージを2回受け取ると終了要求を出す。
        ## これによりweb_mainが2回起動している確認ができる。
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

        ## ついでにログ出力も確認する。
        with self.assertLogs(logger="yt_diffuser.main.main", level="WARNING") as cm:
            self.assertIsNone(process(web_main=web_main, processing_main=processing_main))
            self.assertEqual(cm.output, ['WARNING:yt_diffuser.main.main:Web process is dead. Restarting...'])

        with self.assertLogs(logger="yt_diffuser.main.main", level="WARNING") as cm:
            self.assertIsNone(process(web_main=processing_main, processing_main=web_main))
            self.assertEqual(cm.output, ['WARNING:yt_diffuser.main.main:Processing process is dead. Restarting...'])

if __name__ == "__main__":
    unittest.main()