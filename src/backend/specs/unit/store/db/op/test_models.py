"""
yt_diffuser.store.db.op.models のテスト
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

def test_create_table(conn):
    """
    create_table

    it:
        テーブルを作成する。
    """
    models.create_table(conn)

    # SELECTにエラーが出なければOK
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM models")
    assert cursor.fetchone()[0] == 0

def test_insert(conn):
    """
    insert

    it:
        モデルマスターにモデル情報を挿入する。
    """
    models.create_table(conn)

    models.insert(conn,
        model_name="model_name",
        revision="revision",
        class_name="class_name"
    )

    cursor = conn.cursor()
    cursor.execute("SELECT count(*) FROM models WHERE model_name = 'model_name' AND revision = 'revision' AND class_name = 'class_name'")
    assert cursor.fetchone()[0] == 1


def test_get_all(conn):
    """
    get_all

    it:
        モデルマスターに登録されている全てのモデル情報を取得する。
    """
    models.create_table(conn)
    models.insert(conn, "model_name", "revision", 0)

    result = models.get_all(conn)

    assert len(result) == 1
    assert result[0]["model_name"] == "model_name"
    assert result[0]["revision"] == "revision"
    assert result[0]["class_name"] == 0


def test_get(conn):
    """
    get

    it:
        モデル名とリビジョンからモデルマスター情報を取得する。
    """
    models.create_table(conn)
    models.insert(conn, "model_name", "revision", 0, "screen_name")

    result = models.get(conn, "model_name", "revision")

    assert result["model_name"] == "model_name"
    assert result["revision"] == "revision"
    assert result["class_name"] == 0
    assert result["screen_name"] == "screen_name"


def test_is_exists(conn):
    """
    is_exists

    it:
        指定したモデル名とリビジョンのモデルが存在するか判定する。
    """
    models.create_table(conn)
    models.insert(conn, "model_name", "revision", 0)

    assert models.is_exists(conn, "model_name", "revision") == True
    assert models.is_exists(conn, "none", "revision") == False


def test_update(conn):
    """
    update

    it:
        モデル名とリビジョンからモデルマスター情報を更新する。
    """
    models.create_table(conn)
    models.insert(conn, "model_name", "revision", 0)

    models.update(conn, "model_name", "revision",
        class_name=1,
        screen_name="screen_name"
    )

    result = models.get(conn, "model_name", "revision")

    assert result["class_name"] == 1
    assert result["screen_name"] == "screen_name"

def test_delete(conn):
    """
    delete

    it:
        モデルマスターからモデル情報を削除する。
    """
    models.create_table(conn)
    models.insert(conn, "model_name", "revision", "class_name")

    models.delete(conn, "model_name", "revision")

    assert models.is_exists(conn, "model_name", "revision") == False