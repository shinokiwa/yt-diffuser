""" データベース状態管理 database_status のテーブル操作モジュール
"""
from typing import Dict
from sqlite3 import Connection

# キー名定義
VERSION_KEY = 'version'

def create_table (conn:Connection) -> None:
    """ テーブルを作成
    """
    conn.executescript((
        "CREATE TABLE database_status ("
            "key TEXT PRIMARY KEY,"     # ステータスキー
            "value TEXT"                # ステータス値
        ");"
    ))


def set (conn:Connection, key:str, value:str) -> None:
    """ データベース状態管理に値を挿入
    """
    sql = (
        "INSERT INTO database_status (key, value) VALUES (?, ?)"
        "ON CONFLICT(key) DO UPDATE SET value = ?"
    )
    conn.execute(sql, (key, value, value))
    return


def get (conn:Connection, key:str) -> str:
    """ キー名から情報を取得

    Args:
        conn (Connection): DBコネクション
        key (str): キー名

    Returns:
        str: データベース状態情報
    """
    sql = "SELECT value FROM database_status WHERE key = ?"
    row = conn.execute(sql, (key,)).fetchone()
    if row is None:
        return None
    else:
        return row[0]

def delete (conn: Connection, key:str) -> None:
    """ キー名の情報を削除
    """
    sql = "DELETE FROM database_status WHERE key = ?"
    conn.execute(sql, (key,))
    return