"""SQLite3 データベース操作
"""
from logging import getLogger; logger = getLogger(__name__)
import sqlite3

from injector import inject

from .utils import connect_database
from yt_diffuser.defines.path import AppPath

class Database:
    """
    SQLite3 データベース
    """

    @inject
    def __init__(self, pt:AppPath) -> None:
        """
        コンストラクタ
        """
        self.pt = pt

    def __enter__(self) -> sqlite3.Connection:
        """
        コンテキストマネージャの開始処理
        """
        conn = connect_database(self.pt.DB_FILE)
        return conn

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """
        コンテキストマネージャの終了処理
        """
        pass

def create_table(conn:sqlite3.Connection):
    """
    テーブルを作成する。
    """
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS store (
            key TEXT PRIMARY KEY NOT NULL,
            data BLOB NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT (DATETIME('now', 'localtime')),
            update_at TIMESTAMP NOT NULL DEFAULT (DATETIME('now', 'localtime'))
        )
    """)
    conn.commit()
    conn.close()

def save_store(conn:sqlite3.Connection, key:str, data:bytes):
    """
    データをストアに保存する。
    コミットはしないので、呼び出し元で行うこと。

    Args:
        conn : sqlite3.Connection : DB接続
        key : str : キー
        data : bytes : データ
    """
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO store
            (key, data) VALUES (?, ?)
        ON CONFLICT(key) DO UPDATE
            SET data=excluded.data, update_at=DATETIME('now', 'localtime')
    """, (key, data))

def load_store(conn:sqlite3.Connection, key:str) -> bytes:
    """
    ストアからデータを取得する。

    Args:
        conn : sqlite3.Connection : DB接続
        key : str : キー

    Returns:
        bytes : データ
    """
    cursor = conn.cursor()
    cursor.execute("""
        SELECT data FROM store WHERE key=?
    """, (key,))
    row = cursor.fetchone()
    if row is None:
        return None
    return row["data"]

def delete_store(conn:sqlite3.Connection, key:str):
    """
    ストアからデータを削除する。
    コミットはしないので、呼び出し元で行うこと。

    Args:
        conn : sqlite3.Connection : DB接続
        key : str : キー
    """
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM store WHERE key=?
    """, (key,))