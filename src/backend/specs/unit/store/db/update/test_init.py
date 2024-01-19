""" init.py のテスト
"""
import pytest

from specs.mock.store.db import connect_database

from yt_diffuser.config import AppConfig

def test_init_database():
    """
    init_database
    
    it:
        - DBの初期化を行う
        - テスト内容はconnect_databaseで実行済みなので結果のみ確認する
    """

    conn = connect_database()

    # アサーションの都合テーブルは名前順に並べ替える
    tables = conn.execute('SELECT name FROM sqlite_master WHERE type="table" ORDER BY NAME ASC').fetchall()
    table_names = [table[0] for table in tables]
    assert table_names == [
        "database_status",
        "form_data",
        "model_appends",
        "model_info",
        "prompt_archive",
        "sqlite_sequence"
    ]

    assert conn.execute('SELECT value FROM database_status WHERE key="version" ').fetchone()["value"] == "1"