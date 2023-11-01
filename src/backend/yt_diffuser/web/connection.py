""" Workerプロセスとの接続を管理する
対象の変数を分ける必要があるため、Web側とWorker側で分けている。
"""

from multiprocessing.connection import Connection

_shared_conn:Connection = None

def set_shared_conn(conn:Connection) -> None:
    """ メインプロセスからのコネクションを設定する。

    Args:
        conn (Connection): メインプロセスからのコネクション
    """
    global _shared_conn
    _shared_conn = conn

def get_shared_conn() -> Connection:
    """ メインプロセスからのコネクションを取得する。
    """
    return _shared_conn