"""form_dataテーブルの操作を行うモジュール
"""
import sqlite3

def get_all_form_data(db: sqlite3.Connection) -> dict:
    """全てのフォームデータを取得する

    Args:
        db (sqlite3.Connection): DBコネクション

    Returns:
        dict: フォームデータ
    """
    cursor = db.cursor()
    cursor.execute(
        'SELECT key, value FROM form_data'
    )
    return {
        key: value
        for key, value in cursor.fetchall()
    }

def get_form_data(db: sqlite3.Connection, key: str) -> str:
    """指定したキーのフォームデータを取得する

    Args:
        db (sqlite3.Connection): DBコネクション
        key (str): キー
    """
    cursor = db.cursor()
    cursor.execute(
        'SELECT value FROM form_data WHERE key = ?',
        (key,)
    )
    return cursor.fetchone()[0]

def save_all_form_data(db: sqlite3.Connection, form_data: dict):
    """全てのフォームデータを保存する
    未指定のデータは削除される

    Args:
        db (sqlite3.Connection): DBコネクション
        form_data (dict): フォームデータ
    """
    # データを文字列に変換
    data = {}
    for key, value in form_data.items():
        data[key] = str(value)

    cursor = db.cursor()
    cursor.execute('DELETE FROM form_data')

    cursor.executemany(
        'INSERT OR REPLACE INTO form_data VALUES (?, ?)',
        data.items()
    )
    db.commit()

def save_form_data (db: sqlite3.Connection, key: str, value: str):
    """指定したキーのフォームデータを保存する

    Args:
        db (sqlite3.Connection): DBコネクション
        key (str): キー
        value (str): 値
    """
    # データを文字列に変換
    value = str(value)

    cursor = db.cursor()
    cursor.execute(
        'INSERT OR REPLACE INTO form_data VALUES (?, ?)',
        (key, value)
    )
    db.commit()