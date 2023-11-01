""" connection.pyのテスト """

from multiprocessing.connection import Connection
from yt_diffuser.web.connection import set_shared_conn, get_shared_conn

class TestSetSharedConn:
    """ describe: set_shared_conn メインプロセスからのコネクションを設定する """

    def test_set_shared_conn(self):
        """ it: コネクションを設定する """
        global _shared_conn

        c = Connection(0)
        set_shared_conn(c)
        assert get_shared_conn() == c