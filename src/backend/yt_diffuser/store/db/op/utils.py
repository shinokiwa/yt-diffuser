""" テーブル操作ユーティリティ
"""
import sqlite3

def is_exists_table (conn:sqlite3.Connection, table_name: str) -> bool:
    """指定したテーブルが存在するかどうかを返す
    """
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM sqlite_master WHERE type="table" AND name=?', (table_name,))
    result = cursor.fetchone()

    cursor.close()

    return result is not None