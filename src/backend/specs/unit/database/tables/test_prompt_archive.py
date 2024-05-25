"""
yt_diffuser.database.tables.prompt_archive のテスト
"""
import pytest
from datetime import datetime

from yt_diffuser.database import connect_database
from yt_diffuser.database.tables.prompt_archive import *

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
        - テーブルを作成する。
    """
    # SELECTにエラーが出なければOK
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM prompt_archive")
    assert cursor.fetchone()[0] == 0

def test_insert(conn):
    """
    insert

    it:
        - プロンプト記録を追加する。
    """
    insert(conn, Types.PROMPT, "test_prompt_1")
    insert(conn, Types.NEGATIVE_PROMPT, "test_prompt_2")

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM prompt_archive")
    result = cursor.fetchall()
    assert len(result) == 2
    assert result[0]['prompt'] == "test_prompt_1"
    assert result[0]['type'] == Types.PROMPT.value
    assert result[0]['updated_at'] is not None
    assert result[0]['registed_at'] is not None
    assert result[1]['prompt'] == "test_prompt_2"
    assert result[1]['type'] == Types.NEGATIVE_PROMPT.value

def test_get_by_type(conn):
    """
    get_by_type

    it:
        - 指定した種別のプロンプト記録を取得する。
    """
    conn.execute("INSERT INTO prompt_archive (type, prompt) VALUES ('p', 'test_prompt_1')")
    conn.execute("INSERT INTO prompt_archive (type, prompt) VALUES ('p', 'test_prompt_2')")
    conn.execute("INSERT INTO prompt_archive (type, prompt) VALUES ('n', 'test_prompt_3')")
    conn.execute("INSERT INTO prompt_archive (type, prompt) VALUES ('n', 'test_prompt_4')")

    result = get_by_type(conn, Types.PROMPT)
    assert len(result) == 2
    assert result[0]['prompt'] == "test_prompt_2"
    assert result[0]['type'] == Types.PROMPT.value
    assert result[1]['prompt'] == "test_prompt_1"
    assert result[1]['type'] == Types.PROMPT.value

    result = get_by_type(conn, Types.NEGATIVE_PROMPT)
    assert len(result) == 2
    assert result[0]['prompt'] == "test_prompt_4"
    assert result[0]['type'] == Types.NEGATIVE_PROMPT.value
    assert result[1]['prompt'] == "test_prompt_3"
    assert result[1]['type'] == Types.NEGATIVE_PROMPT.value

def test_update(conn):
    """
    update

    it:
        - プロンプト記録を更新する。
        - 今のところは最終更新日時を更新するだけ。
    """
    conn.execute("INSERT INTO prompt_archive (type, prompt, updated_at) VALUES ('p', 'test_prompt_1', '2000-01-01 00:00:00')")
    conn.execute("INSERT INTO prompt_archive (type, prompt, updated_at) VALUES ('n', 'test_prompt_2', '2000-01-01 00:00:00')")

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM prompt_archive")
    result = cursor.fetchall()
    assert result[0]['updated_at'] == result[1]['updated_at']

    update(conn, result[0]['id'])

    cursor.execute("SELECT * FROM prompt_archive")
    result = cursor.fetchall()
    assert result[0]['updated_at'] != result[1]['updated_at']

def test_delete(conn):
    """
    delete

    it:
        - プロンプト記録を削除する。
    """
    conn.execute("INSERT INTO prompt_archive (type, prompt) VALUES ('p', 'test_prompt_1')")
    conn.execute("INSERT INTO prompt_archive (type, prompt) VALUES ('n', 'test_prompt_2')")

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM prompt_archive")
    result = cursor.fetchall()
    assert len(result) == 2

    delete(conn, result[0]['id'])

    cursor.execute("SELECT * FROM prompt_archive")
    result = cursor.fetchall()
    assert len(result) == 1
    assert result[0]['prompt'] == "test_prompt_2"