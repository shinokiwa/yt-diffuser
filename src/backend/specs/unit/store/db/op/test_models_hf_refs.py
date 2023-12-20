"""
yt_diffuser.store.db.op.models_hf_refs のテスト
"""
import pytest

from yt_diffuser.store.db import connect_database
from yt_diffuser.store.db.op import models_hf_refs
from yt_diffuser.store.db.op import models_hf_snapshots
from yt_diffuser.store.db.op import models

@pytest.fixture(scope="function")
def conn():
    """ テスト用のDBコネクションを作成する
    """
    conn = connect_database(":memory:")
    models_hf_refs.create_table(conn)
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
    cursor.execute("SELECT COUNT(*) FROM models_hf_refs")
    assert cursor.fetchone()[0] == 0

def test_insert(conn):
    """
    insert

    it:
        リビジョン参照を挿入する。
    """
    model_id = 1
    commit_hash = "abc123"
    models_hf_refs.insert(conn, model_id, commit_hash)

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM models_hf_refs WHERE model_id = ? AND commit_hash = ?", (model_id, commit_hash))
    assert cursor.fetchone() is not None

def test_get(conn):
    """
    get

    it:
        モデルIDに対応するリビジョン参照を取得する。
    """
    model_id = 1
    commit_hash = "abc123"
    conn.execute("INSERT INTO models_hf_refs (model_id, commit_hash) VALUES (?, ?)", (model_id, commit_hash))

    result = models_hf_refs.get(conn, model_id)
    assert result["model_id"] == model_id
    assert result["commit_hash"] == commit_hash

def test_update(conn):
    """
    update

    it:
        レコードを更新する。
    """
    model_id = 1
    commit_hash = "abc123"
    conn.execute("INSERT INTO models_hf_refs (model_id, commit_hash) VALUES (?, ?)", (model_id, commit_hash))

    new_commit_hash = "def456"
    models_hf_refs.update(conn, model_id, new_commit_hash)

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM models_hf_refs WHERE model_id = ? AND commit_hash = ?", (model_id, new_commit_hash))
    assert cursor.fetchone() is not None

def test_delete(conn):
    """
    delete

    it:
        リビジョン参照を削除する。
    """
    model_id = 1
    commit_hash = "abc123"
    models_hf_refs.insert(conn, model_id, commit_hash)

    models_hf_refs.delete(conn, model_id)

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM models_hf_refs WHERE model_id = ? AND commit_hash = ?", (model_id, commit_hash))
    assert cursor.fetchone() is None

def test_cleanup(conn):
    """
    cleanup

    it:
        参照先が削除された参照を削除する。
        modelsもmodels_hf_snapshotsも存在する場合
    """
    models.create_table(conn)
    models_hf_snapshots.create_table(conn)

    commit_hash = "abc123"

    models.insert(conn, "model_name", "revision", 0)
    model_id = models.get(conn, "model_name", "revision")["id"]
    models_hf_snapshots.insert(conn, model_id, commit_hash)
    models_hf_refs.insert(conn, model_id, commit_hash)

    models_hf_refs.cleanup(conn)

    result = conn.execute("SELECT * FROM models_hf_refs WHERE model_id = ? AND commit_hash = ?", (model_id, commit_hash)).fetchall()
    assert len(result) == 1

def test_cleanup2(conn):
    """
    cleanup

    it:
        参照先が削除された参照を削除する。
        modelsがない場合
    """
    models.create_table(conn)
    models_hf_snapshots.create_table(conn)

    model_id = 1
    commit_hash = "abc123"

    models_hf_refs.insert(conn, model_id, commit_hash)
    models_hf_snapshots.insert(conn, model_id, commit_hash)

    models_hf_refs.cleanup(conn)

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM models_hf_refs WHERE model_id = ? AND commit_hash = ?", (model_id, commit_hash))
    assert cursor.fetchone() is None

def test_cleanup3(conn):
    """
    cleanup

    it:
        参照先が削除された参照を削除する。
        models_hf_snapshotsがない場合
    """
    models.create_table(conn)
    models_hf_snapshots.create_table(conn)

    commit_hash = "abc123"

    models.insert(conn, "model_name", "revision", 0)
    model_id = models.get(conn, "model_name", "revision")["id"]
    models_hf_refs.insert(conn, model_id, commit_hash)

    models_hf_refs.cleanup(conn)
    
    assert conn.execute("SELECT * FROM models_hf_refs WHERE model_id = ? AND commit_hash = ?", (model_id, commit_hash)).fetchone() is None

def test_cleanup4(conn):
    """
    cleanup

    it:
        参照先が削除された参照を削除する。
        modelsもmodels_hf_snapshotsも存在しない場合
    """
    models.create_table(conn)
    models_hf_snapshots.create_table(conn)

    commit_hash = "abc123"

    models_hf_refs.insert(conn, 1, commit_hash)

    models_hf_refs.cleanup(conn)

    assert conn.execute("SELECT * FROM models_hf_refs WHERE model_id = ? AND commit_hash = ?", (1, commit_hash)).fetchone() is None