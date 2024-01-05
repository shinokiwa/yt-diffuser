"""
テスト用ユーティリティ

DB関係。
"""
from sqlite3 import Connection

from yt_diffuser.store.db import connect_database
from yt_diffuser.store.db.setup import setup_database
from yt_diffuser.store.db.update.init import init_database

from yt_diffuser.config import AppConfig

def make_db(config:AppConfig) -> Connection:
    """
    テスト用のDBをセットアップする。
    """
    setup_database(config.DB_FILE, config.DB_UPDATE_FILE, config.DB_VERSION)
    conn = connect_database(config.DB_FILE)
    return conn

def make_db_memory(config:AppConfig) -> Connection:
    """
    テスト用のインメモリDBをセットアップする。
    """
    conn = connect_database(":memory:")
    init_database(conn, config.DB_VERSION)

    return conn