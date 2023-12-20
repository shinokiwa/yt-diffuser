"""
リビジョン参照テーブル models_hf_refs

models.revision がコミットハッシュでない場合、
models_hf_snapshots.commit_hash との紐づけをこのテーブルで行う。
"""
from typing import Dict, List
from sqlite3 import Connection


def create_table (conn:Connection) -> None:
    """
    テーブルを作成する。

    Args:
        conn (Connection): DBコネクション
    """
    conn.executescript((
        "CREATE TABLE models_hf_refs ("
            "model_id        INTEGER     NOT NULL    PRIMARY KEY,"               # 対応するモデルID
            "commit_hash     TEXT        NOT NULL,"                              # コミットハッシュ
            "updated_at      DATETIME    NOT NULL    DEFAULT CURRENT_TIMESTAMP," # レコードの更新日時
            "registed_at     DATETIME    NOT NULL    DEFAULT CURRENT_TIMESTAMP"  # レコードの登録日時
        ");"
        # インデックス
        "CREATE INDEX models_hf_refs_commit_hash ON models_hf_refs (commit_hash);"
    ))

def insert (conn:Connection, model_id:int, commit_hash:str) -> None:
    """
    リビジョン参照を挿入する。

    Args:
        conn (Connection): DBコネクション
        model_id (int): モデルID
        commit_hash (str): コミットハッシュ
    """
    sql = "INSERT INTO models_hf_refs (model_id, commit_hash) VALUES (?, ?)"
    conn.execute(sql, (model_id, commit_hash))
    return

def get (conn:Connection, model_id:int) -> Dict:
    """
    モデルIDに対応するリビジョン参照を取得する。

    Args:
        conn (Connection): DBコネクション
        model_id (int): モデルID

    Returns:
        Dict: リビジョン参照
            - model_id: モデルID
            - commit_hash: コミットハッシュ
            - updated_at: レコードの更新日時
"""
    sql = "SELECT model_id, commit_hash, updated_at FROM models_hf_refs WHERE model_id = ?"
    return conn.execute(sql, (model_id,)).fetchone()


def update (conn:Connection, model_id:int, commit_hash:str) -> None:
    """
    リビジョン参照を更新する。

    Args:
        conn (Connection): DBコネクション
        model_id (int): モデルID
        commit_hash (str): コミットハッシュ
    """
    sql = "UPDATE models_hf_refs SET commit_hash = ? WHERE model_id = ?"
    conn.execute(sql, (commit_hash, model_id))
    return

def delete (conn:Connection, model_id:int) -> None:
    """
    リビジョン参照を削除する。

    Args:
        conn (Connection): DBコネクション
        model_id (int): モデルID
    """
    sql = "DELETE FROM models_hf_refs WHERE model_id = ?"
    conn.execute(sql, (model_id,))
    return

def cleanup (conn:Connection) -> None:
    """
    参照先が削除された参照を削除する。

    Args:
        conn (Connection): DBコネクション
    """
    sql = "DELETE FROM models_hf_refs WHERE " \
        "model_id NOT IN (SELECT id FROM models) OR " \
        "commit_hash NOT IN (SELECT commit_hash FROM models_hf_snapshots)"
    conn.execute(sql)
    return