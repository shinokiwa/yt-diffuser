""" model.py のテスト
"""
import pytest

from yt_diffuser.store.db import connect_database
from yt_diffuser.store.db.op import models

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
    models.create_table(conn)

    # SELECTにエラーが出なければOK
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM models")
    assert cursor.fetchone()[0] == 0

@pytest.mark.describe("insert")
@pytest.mark.it("データが挿入される")
def test_insert(conn):
    models.create_table(conn)

    models.insert(conn, "path", "name", "revision", "class_name")

    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM models")
    assert cursor.fetchone()[0] == 1


@pytest.mark.describe("get_by_pathname")
@pytest.mark.it("パス名からモデル情報を取得できる")
def test_get_by_pathname(conn):
    models.create_table(conn)
    models.insert(conn, "path", "name", "revision", "class_name")

    result = models.get_by_pathname(conn, "path")

    assert result["path_name"] == "path"
    assert result["name"] == "name"
    assert result["revision"] == "revision"
    assert result["class_name"] == "class_name"

@pytest.mark.describe("is_exists_by_pathname")
@pytest.mark.it("パス名のモデルが存在するか判定できる")
def test_is_exists_by_pathname(conn):
    models.create_table(conn)
    models.insert(conn, "path", "name", "revision", "class_name")

    assert models.is_exists_by_pathname(conn, "path") == True
    assert models.is_exists_by_pathname(conn, "path2") == False

@pytest.mark.describe("update_by_pathname")
@pytest.mark.it("パス名からモデル情報を更新できる")
def test_update_by_pathname(conn):
    models.create_table(conn)
    models.insert(conn, "path", "name", "revision", "class_name")

    models.update_by_pathname(conn, "path", name="new_name", revision="new_revision", class_name="new_class_name")

    result = models.get_by_pathname(conn, "path")

    assert result["name"] == "new_name"
    assert result["revision"] == "new_revision"
    assert result["class_name"] == "new_class_name"

@pytest.mark.describe("delete_by_pathname")
@pytest.mark.it("パス名からモデル情報を削除できる")
def test_delete_by_pathname(conn):
    models.create_table(conn)
    models.insert(conn, "path", "name", "revision", "class_name")

    models.delete_by_pathname(conn, "path")

    assert models.is_exists_by_pathname(conn, "path") == False