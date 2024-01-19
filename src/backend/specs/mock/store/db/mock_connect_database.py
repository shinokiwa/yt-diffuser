"""
connect_databaseをテスト用にモック化する
"""
from sqlite3 import Connection
from pathlib import Path

from yt_diffuser.store.db import connect_database as _connect_database
from yt_diffuser.store.db.update.init import init_database

def connect_database (db_file:Path = None) -> Connection:
    """
    テスト用のDBをセットアップする。
    引数を指定しない場合はインメモリDBをセットアップする。
    """
    if db_file is None:
        db_file = ":memory:"
    conn = _connect_database(db_file)
    init_database(conn, 1)

    return conn