"""
yt_diffuser.store.db.op.models_hf_snapshots のテスト
"""
import pytest

from yt_diffuser.store.db import connect_database
from yt_diffuser.store.db.op import models_hf_snapshots
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
    models_hf_snapshots.create_table(conn)

    # SELECTにエラーが出なければOK
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM models_hf_snapshots")
    assert cursor.fetchone()[0] == 0

def test_insert(conn):
    """
    insert

    it:
        スナップショット情報を挿入する。
        
    """
    models_hf_snapshots.create_table(conn)

    models_hf_snapshots.insert(conn,
        model_id=1,
        commit_hash="commit_hash"
    )

    cursor = conn.cursor()
    cursor.execute("SELECT count(*) FROM models_hf_snapshots WHERE model_id = 1 AND commit_hash = 'commit_hash'")
    assert cursor.fetchone()[0] == 1


def test_find_by_model_id(conn):
    """
    find_by_model_id

    it:
        モデルIDに対応するスナップショット情報を取得する。
    """
    models_hf_snapshots.create_table(conn)
    models_hf_snapshots.insert(conn, 1, "commit_hash")

    result = models_hf_snapshots.find_by_model_id(conn, 1)

    assert result[0]["model_id"] == 1
    assert result[0]["commit_hash"] == "commit_hash"

def test_find_by_commit_hash(conn):
    """
    find_by_commit_hash

    it:
        コミットハッシュに対応するスナップショット情報を取得する。
    """
    models_hf_snapshots.create_table(conn)
    models_hf_snapshots.insert(conn, 1, "commit_hash")

    result = models_hf_snapshots.find_by_commit_hash(conn, "commit_hash")

    assert result[0]["model_id"] == 1
    assert result[0]["commit_hash"] == "commit_hash"


def test_is_exists(conn):
    """
    is_exists

    it:
        モデルIDとコミットハッシュに対応するスナップショット情報が存在するか判定する。
    """
    models_hf_snapshots.create_table(conn)
    models_hf_snapshots.insert(conn, 1, "commit_hash")

    assert models_hf_snapshots.is_exists(conn, 1, "commit_hash") == True
    assert models_hf_snapshots.is_exists(conn, 1, "commit_hash2") == False


def test_delete(conn):
    """
    delete

    it:
        モデルIDとコミットハッシュに対応するスナップショット情報を削除する。
    """
    models_hf_snapshots.create_table(conn)
    models_hf_snapshots.insert(conn, 1, "commit_hash")

    models_hf_snapshots.delete(conn, 1, "commit_hash")

    cursor = conn.cursor()
    cursor.execute("SELECT count(*) FROM models_hf_snapshots WHERE model_id = 1 AND commit_hash = 'commit_hash'")
    assert cursor.fetchone()[0] == 0

def test_cleanup (conn):
    """
    cleanup

    it:
        モデルマスターに存在しないスナップショット情報を削除する。
    """
    models_hf_snapshots.create_table(conn)
    models.create_table(conn)

    models.insert(conn, "model_name", "revision", 0)
    models_hf_snapshots.insert(conn, 1, "commit_hash")
    models_hf_snapshots.insert(conn, 2, "commit_hash2")
    models_hf_snapshots.insert(conn, 3, "commit_hash3")

    models_hf_snapshots.cleanup(conn)

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM models_hf_snapshots")
    result = cursor.fetchall()

    assert len(result) == 1
    assert result[0]["model_id"] == 1
    assert result[0]["commit_hash"] == "commit_hash"

