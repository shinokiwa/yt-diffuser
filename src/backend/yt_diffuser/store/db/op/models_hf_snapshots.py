"""
スナップショット情報テーブル models_hf_snapshots

HuggingFace Snapshotsごとの情報を保存する。
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
        "CREATE TABLE models_hf_snapshots ("
            "id              INTEGER     NOT NULL    PRIMARY KEY AUTOINCREMENT," # スナップショットID
            "model_id        INTEGER     NOT NULL,"                              # 対応するモデルID
            "commit_hash     TEXT        NOT NULL,"                              # コミットハッシュ
            "updated_at      DATETIME    NOT NULL    DEFAULT CURRENT_TIMESTAMP," # レコードの更新日時
            "registed_at     DATETIME    NOT NULL    DEFAULT CURRENT_TIMESTAMP"  # レコードの登録日時
        ");"
        # インデックス
        "CREATE UNIQUE INDEX models_hf_snapshots_hash ON models_hf_snapshots (model_id, commit_hash);"
        "CREATE INDEX models_hf_snapshots_model_id ON models_hf_snapshots (model_id);"
        "CREATE INDEX models_hf_snapshots_commit_hash ON models_hf_snapshots (commit_hash);"
    ))

def insert (conn:Connection, model_id:int, commit_hash:str) -> None:
    """
    スナップショット情報を挿入する。

    Args:
        conn (Connection): DBコネクション
        model_id (int): モデルID
        commit_hash (str): コミットハッシュ
    
    Returns:
        None
    """
    sql = "INSERT INTO models_hf_snapshots (model_id, commit_hash) VALUES (?, ?)"
    conn.execute(sql, (model_id, commit_hash))
    return

def find_by_model_id (conn:Connection, model_id:int) -> List[Dict]:
    """
    モデルIDに対応するスナップショット情報を取得する。

    Args:
        conn (Connection): DBコネクション
        model_id (int): モデルID

    Returns:
        List[Dict]: スナップショット情報のリスト
            - id: スナップショットID
            - model_id: モデルID
            - commit_hash: コミットハッシュ
            - updated_at: レコードの更新日時
            - registed_at: レコードの登録日時
    """
    sql = "SELECT * FROM models_hf_snapshots WHERE model_id = ?"
    return conn.execute(sql, (model_id,)).fetchall()

def find_by_commit_hash (conn:Connection, commit_hash:str) -> List[Dict]:
    """
    コミットハッシュに対応するスナップショット情報を取得する。

    Args:
        conn (Connection): DBコネクション
        commit_hash (str): コミットハッシュ

    Returns:
        List[Dict]: スナップショット情報のリスト
            - id: スナップショットID
            - model_id: モデルID
            - commit_hash: コミットハッシュ
            - updated_at: レコードの更新日時
            - registed_at: レコードの登録日時
    """
    sql = "SELECT * FROM models_hf_snapshots WHERE commit_hash = ?"
    return conn.execute(sql, (commit_hash,)).fetchall()


def is_exists (conn:Connection, model_id:int, commit_hash:str) -> bool:
    """
    モデルIDとコミットハッシュに対応するスナップショット情報が存在するか判定する。

    Args:
        conn (Connection): DBコネクション
        model_id (int): モデルID
        commit_hash (str): コミットハッシュ

    Returns:
        bool: 存在する場合はTrue、存在しない場合はFalse
    """
    sql = "SELECT COUNT(*) FROM models_hf_snapshots WHERE model_id = ? AND commit_hash = ?"
    return conn.execute(sql, (model_id, commit_hash,)).fetchone()[0] > 0


def delete (conn:Connection, model_id:int, commit_hash:str) -> None:
    """
    モデルIDとコミットハッシュに対応するスナップショット情報を削除する。

    Args:
        conn (Connection): DBコネクション
        model_id (int): モデルID
        commit_hash (str): コミットハッシュ
    
    Returns:
        None
    """
    sql = "DELETE FROM models_hf_snapshots WHERE model_id = ? AND commit_hash = ?"
    conn.execute(sql, (model_id, commit_hash))
    return


def cleanup (conn:Connection) -> None:
    """
    モデルマスターに存在しないスナップショット情報を削除する。

    Args:
        conn (Connection): DBコネクション
    """
    sql = (
        "DELETE FROM models_hf_snapshots WHERE model_id NOT IN ("
            "SELECT id FROM models"
        ");"
    )
    conn.execute(sql)
    return