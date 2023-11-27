""" database_status.py のテスト
"""
import pytest

from yt_diffuser.store.db import connect_database
from yt_diffuser.store.db.op import database_status

@pytest.fixture(scope="function")
def conn():
    """ テスト用のDBコネクションを作成する
    """
    conn = connect_database(":memory:")
    yield conn
    conn.close()

@pytest.mark.describe("create_table")
@pytest.mark.it("テーブルが作成される")
def test_create_table(conn):
    database_status.create_table(conn)

    # SELECTにエラーが出なければOK
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM database_status")
    assert cursor.fetchone()[0] == 0

@pytest.mark.describe("set")
@pytest.mark.it("データが挿入される")
@pytest.mark.it("すでに存在するキーの場合は更新される")
def test_set(conn):
    database_status.create_table(conn)

    database_status.set(conn, "key", "value")

    cursor = conn.cursor()
    cursor.execute("SELECT value FROM database_status WHERE key = ?", ("key",))
    assert cursor.fetchone()[0] == "value"

    database_status.set(conn, "key", "value2")

    cursor = conn.cursor()
    cursor.execute("SELECT value FROM database_status WHERE key = ?", ("key",))
    assert cursor.fetchone()[0] == "value2"

@pytest.mark.describe("get")
@pytest.mark.it("キー名から情報を取得できる")
@pytest.mark.it("存在しないキー名の場合はNoneが返る")
def test_get(conn):
    database_status.create_table(conn)

    conn.execute("INSERT INTO database_status (key, value) VALUES (?, ?)", ("key", "value"))

    assert database_status.get(conn, "key") == "value"
    assert database_status.get(conn, "key2") == None

@pytest.mark.describe("delete")
@pytest.mark.it("キー名の情報を削除できる")
def test_delete(conn):
    database_status.create_table(conn)

    conn.execute("INSERT INTO database_status (key, value) VALUES (?, ?)", ("key", "value"))

    database_status.delete(conn, "key")

    cursor = conn.cursor()
    cursor.execute("SELECT value FROM database_status WHERE key = ?", ("key",))
    assert cursor.fetchone() == None

