""" init.py のテスト
"""
import pytest

from specs.utils.test_utils.db import make_db_memory

from yt_diffuser.config import AppConfig

def test_init_database():
    """
    init_database
    
    it:
        - DBの初期化を行う
        - テスト内容はmake_db_memoryと同じなので結果だけ確認する
    """

    conn = make_db_memory(AppConfig())

    # アサーションの都合テーブルは名前順に並べ替える
    tables = conn.execute('SELECT name FROM sqlite_master WHERE type="table" ORDER BY NAME ASC').fetchall()
    table_names = [table[0] for table in tables]
    assert table_names == [
        "database_status",
        "form_data",
        "model_info",
        "prompt_archive",
        "sqlite_sequence"
    ]

    assert conn.execute('SELECT value FROM database_status WHERE key="version" ').fetchone()["value"] == "1"