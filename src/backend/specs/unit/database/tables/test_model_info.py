"""
yt_diffuser.database.tables.model_info のテスト
"""
import pytest

from yt_diffuser.database import connect_database
from yt_diffuser.database.tables.model_info import *

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
    cursor.execute("SELECT COUNT(*) FROM model_info")
    assert cursor.fetchone()[0] == 0


def test_save(conn):
    """
    save

    it:
        - モデルマスターにモデル情報を保存する。
        - レコードが存在する場合は更新、存在しない場合は追加する。
    """
    save(conn,
        model_name="model_name",
        class_name=ModelClass.BASE_MODEL,
        screen_name="screen_name"
    )

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM model_info WHERE model_name = 'model_name'")
    result = cursor.fetchall()
    assert len(result) == 1
    assert result[0][0] == "model_name"
    assert result[0][1] == ModelClass.BASE_MODEL.value
    assert result[0][2] == "screen_name"


    save(conn,
        model_name="model_name",
        class_name=ModelClass.LORA_MODEL,
        screen_name="screen_name2"
    )

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM model_info WHERE model_name = 'model_name'")
    result = cursor.fetchall()
    assert len(result) == 1
    assert result[0][0] == "model_name"
    assert result[0][1] == ModelClass.LORA_MODEL.value
    assert result[0][2] == "screen_name2"


def test_get(conn):
    """
    get

    it:
        モデル名とリビジョンからモデルマスター情報を取得する。
    """
    conn.execute("INSERT INTO model_info (model_name, class_name, screen_name) VALUES ('model_name', '" + ModelClass.BASE_MODEL.value + "', 'screen_name')")

    result = get(conn, "model_name")

    assert result["model_name"] == "model_name"
    assert ModelClass(result["class_name"]) == ModelClass.BASE_MODEL
    assert result["screen_name"] == "screen_name"


def test_delete(conn):
    """
    delete

    it:
        モデルマスターからモデル情報を削除する。
    """
    conn.execute("INSERT INTO model_info (model_name, class_name, screen_name) VALUES ('model_name', 'class_name', 'screen_name')")

    delete(conn, "model_name")

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM model_info WHERE model_name = 'model_name'")
    result = cursor.fetchall()
    assert len(result) == 0