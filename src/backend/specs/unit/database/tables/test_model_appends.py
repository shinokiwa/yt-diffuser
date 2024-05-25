"""
yt_diffuser.database.tables.model_appends のテスト
"""
import pytest

from yt_diffuser.database import connect_database
from yt_diffuser.database.tables.model_appends import *

@pytest.fixture(scope="function")
def conn():
    """ テスト用のDBコネクションを作成する
    """
    conn = connect_database(":memory:")
    create_table(conn)
    yield conn
    conn.close()

def test_create_table(conn):
    """
    create_table

    it:
        テーブルを作成する。
    """
    # SELECTにエラーが出なければOK
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM model_appends")
    assert cursor.fetchone()[0] == 0


def test_save(conn):
    """
    save

    it:
        - モデル追加情報を保存する。
        - レコードが存在する場合は更新、存在しない場合は追加する。
    """
    save(conn,
        model_name="model_name",
        key="key",
        value="value"
    )

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM model_appends WHERE model_name = 'model_name'")
    result = cursor.fetchall()
    assert len(result) == 1
    assert result[0][0] == "model_name"
    assert result[0][1] == "key"
    assert result[0][2] == "value"


    save(conn,
        model_name="model_name",
        key="key",
        value="value2"
    )

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM model_appends WHERE model_name = 'model_name'")
    result = cursor.fetchall()
    assert len(result) == 1
    assert result[0][0] == "model_name"
    assert result[0][1] == "key"
    assert result[0][2] == "value2"


def test_get(conn):
    """
    get

    it:
        モデル名からモデル追加情報を取得する。
    """
    conn.execute("INSERT INTO model_appends (model_name, key, value) VALUES (?, ?, ?)", ("model_name", "key", "value"))
    conn.execute("INSERT INTO model_appends (model_name, key, value) VALUES (?, ?, ?)", ("model_name", "key2", "value2"))

    result = get(conn, "model_name")
    assert result == {"key": "value", "key2": "value2"}


def test_delete(conn):
    """
    delete

    it:
        モデル追加情報を削除する。
    """
    conn.execute("INSERT INTO model_appends (model_name, key, value) VALUES (?, ?, ?)", ("model_name", "key", "value"))
    conn.execute("INSERT INTO model_appends (model_name, key, value) VALUES (?, ?, ?)", ("model_name", "key2", "value2"))

    delete(conn, "model_name", "key")

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM model_appends WHERE model_name = 'model_name'")
    result = cursor.fetchall()
    assert len(result) == 1
    assert result[0][0] == "model_name"
    assert result[0][1] == "key2"
    assert result[0][2] == "value2"


def test_delete_all(conn):
    """
    delete_all

    it:
        モデル追加情報を全て削除する。
    """
    conn.execute("INSERT INTO model_appends (model_name, key, value) VALUES (?, ?, ?)", ("model_name", "key", "value"))
    conn.execute("INSERT INTO model_appends (model_name, key, value) VALUES (?, ?, ?)", ("model_name", "key2", "value2"))
    conn.execute("INSERT INTO model_appends (model_name, key, value) VALUES (?, ?, ?)", ("model_name2", "key", "value"))

    delete_all(conn, "model_name")

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM model_appends")
    result = cursor.fetchall()
    assert len(result) == 1
    assert result[0][0] == "model_name2"