""" init.py のテスト
"""
import pytest

from yt_diffuser.store.db.update.init import init_database
from yt_diffuser.store.db import connect_database

@pytest.mark.describe("init_database")
@pytest.mark.it("DBの初期化を行う")
def test_init_database(mocker):

    conn = connect_database(":memory:")
    db_version = 1
    
    init_database(conn, db_version)

    tables = conn.execute('SELECT name FROM sqlite_master WHERE type="table" ORDER BY NAME ASC').fetchall()
    table_names = [table[0] for table in tables]
    assert table_names == [
        "database_status",
        "models",
        "sqlite_sequence"
    ]

    assert conn.execute('SELECT value FROM database_status WHERE key="version" ').fetchone()["value"] == "1"