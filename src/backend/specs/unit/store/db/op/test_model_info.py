"""
yt_diffuser.store.db.op.models のテスト
"""
import pytest

from yt_diffuser.store.db import connect_database
from yt_diffuser.store.db.op import model_info

@pytest.fixture(scope="function")
def conn():
    """ テスト用のDBコネクションを作成する
    """
    conn = connect_database(":memory:")
    model_info.create_table(conn)
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
    cursor.execute("SELECT COUNT(*) FROM model_info")
    assert cursor.fetchone()[0] == 0


def test_save(conn):
    """
    save

    it:
        - モデルマスターにモデル情報を保存する。
        - レコードが存在する場合は更新、存在しない場合は追加する。
    """
    model_info.save(conn,
        model_name="model_name",
        revision="revision",
        class_name="class_name",
        screen_name="screen_name"
    )

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM model_info WHERE model_name = 'model_name' AND revision = 'revision'")
    result = cursor.fetchall()
    assert len(result) == 1
    assert result[0][0] == "model_name"
    assert result[0][1] == "revision"
    assert result[0][2] == "class_name"
    assert result[0][3] == "screen_name"


    model_info.save(conn,
        model_name="model_name",
        revision="revision",
        class_name="class_name2",
        screen_name="screen_name2"
    )

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM model_info WHERE model_name = 'model_name' AND revision = 'revision'")
    result = cursor.fetchall()
    assert len(result) == 1
    assert result[0][0] == "model_name"
    assert result[0][1] == "revision"
    assert result[0][2] == "class_name2"
    assert result[0][3] == "screen_name2"


def test_get(conn):
    """
    get

    it:
        モデル名とリビジョンからモデルマスター情報を取得する。
    """
    conn.execute("INSERT INTO model_info (model_name, revision, class_name, screen_name) VALUES ('model_name', 'revision', 'class_name', 'screen_name')")

    result = model_info.get(conn, "model_name", "revision")

    assert result["model_name"] == "model_name"
    assert result["revision"] == "revision"
    assert result["class_name"] == "class_name"
    assert result["screen_name"] == "screen_name"


def test_delete(conn):
    """
    delete

    it:
        モデルマスターからモデル情報を削除する。
    """
    conn.execute("INSERT INTO model_info (model_name, revision, class_name, screen_name) VALUES ('model_name', 'revision', 'class_name', 'screen_name')")

    model_info.delete(conn, "model_name", "revision")

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM model_info WHERE model_name = 'model_name' AND revision = 'revision'")
    result = cursor.fetchall()
    assert len(result) == 0