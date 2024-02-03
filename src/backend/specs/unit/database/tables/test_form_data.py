"""
yt_diffuser.database.tables.form_data のテスト
"""
import pytest

from yt_diffuser.database import connect_database
from yt_diffuser.database.tables.form_data import *

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
    cursor.execute("SELECT COUNT(*) FROM form_data")
    assert cursor.fetchone()[0] == 0


def test_save(conn):
    """
    save

    it:
        - フォーム情報を保存する。
        - レコードが存在する場合は更新、存在しない場合は追加する。
    """
    save(conn,
        test_name_1="test_value_1",
        test_name_2="test_value_2",
    )

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM form_data")
    result = cursor.fetchall()
    assert len(result) == 2
    assert result[0]['name'] == "test_name_1"
    assert result[0]['value'] == "test_value_1"
    assert result[0]['updated_at'] is not None
    assert result[0]['registed_at'] is not None
    assert result[1]['name'] == "test_name_2"
    assert result[1]['value'] == "test_value_2"

    save(conn,
        test_name_1="test_value_1_1",
        test_name_3="test_value_3",
    )


    cursor = conn.cursor()
    cursor.execute("SELECT * FROM form_data")
    result = cursor.fetchall()
    assert len(result) == 3
    assert result[0]['name'] == "test_name_1"
    assert result[0]['value'] == "test_value_1_1"
    assert result[1]['name'] == "test_name_2"
    assert result[1]['value'] == "test_value_2"
    assert result[2]['name'] == "test_name_3"
    assert result[2]['value'] == "test_value_3"


def test_get_all(conn):
    """
    get_all

    it:
        - フォーム情報を全て取得する。
    """
    conn.execute(
        "INSERT INTO form_data"
        " (name, value) VALUES"
        " ('test_name_1', 'test_value_1')"
        ",('test_name_2', 'test_value_2')"
        )
                 
    result = get_all(conn)

    assert result == {
        'test_name_1': 'test_value_1',
        'test_name_2': 'test_value_2',
    }


def test_delete(conn):
    """
    delete

    it:
        - フォーム情報を削除する。
    """
    conn.execute(
        "INSERT INTO form_data"
        " (name, value) VALUES"
        " ('test_name_1', 'test_value_1')"
        ",('test_name_2', 'test_value_2')"
        )

    delete(conn, "test_name_1")

    result = conn.execute("SELECT * FROM form_data").fetchall()

    assert len(result) == 1
    assert result[0]['name'] == "test_name_2"
    assert result[0]['value'] == "test_value_2"


def test_delete_not_in(conn):
    """
    delete_not_in
    
    it:
        - 指定したフォーム名以外のフォーム情報を削除する。
    """
    conn.execute(
        "INSERT INTO form_data"
        " (name, value) VALUES"
        " ('test_name_1', 'test_value_1')"
        ",('test_name_2', 'test_value_2')"
        ",('test_name_3', 'test_value_3')"
        )

    delete_not_in(conn, ['test_name_1', 'test_name_2'])

    result = conn.execute("SELECT * FROM form_data").fetchall()

    assert len(result) == 2
    assert result[0]['name'] == "test_name_1"
    assert result[0]['value'] == "test_value_1"
    assert result[1]['name'] == "test_name_2"
    assert result[1]['value'] == "test_value_2"