"""
モデル情報マスターテーブル models
"""
from typing import Dict, List
from sqlite3 import Connection

from yt_diffuser.store import MODEL_CLASS_NAME

def create_table (conn:Connection) -> None:
    """
    テーブルを作成する。

    Args:
        conn (Connection): DBコネクション
    """
    conn.executescript((
        "CREATE TABLE models ("
            "id              INTEGER     NOT NULL    PRIMARY KEY AUTOINCREMENT," # モデルID
            "model_name      TEXT        NOT NULL,"                              # モデル名
            "revision        TEXT        NOT NULL,"                              # モデルのリビジョン
            "class_name      INT         NOT NULL,"                              # このモデルを処理するクラス
            "screen_name     TEXT,"                                              # モデルの表示名
            "updated_at      DATETIME    NOT NULL    DEFAULT CURRENT_TIMESTAMP," # モデルの更新日時
            "registed_at     DATETIME    NOT NULL    DEFAULT CURRENT_TIMESTAMP"  # モデルの登録日時
        ");"
        # インデックス
        "CREATE UNIQUE INDEX models_path ON models (model_name, revision);"
        "CREATE INDEX models_model_name ON models (model_name);"
        "CREATE INDEX models_class ON models (class_name);"
    ))


MODEL_DEFAULT_REVISION = "0" # モデルのリビジョンのデフォルト値

def insert (conn:Connection, model_name:str, revision:str, class_name:int, screen_name:str = "") -> None:
    """
    モデルマスターにモデル情報を挿入する。

    Args:
        conn (Connection): DBコネクション
        model_name (str): モデル名
        revision (str): モデルのリビジョン
        class_name (int): このモデルを処理するクラス(定数 MODEL_CLASS_NAME のいずれか)
        screen_name (str): モデルの表示名
    
    Returns:
        None
    """
    sql = "INSERT INTO models (model_name, revision, class_name, screen_name) VALUES (?, ?, ?, ?)"
    conn.execute(sql, (model_name, revision, class_name, screen_name))
    return

def get_all (conn:Connection) -> List[Dict]:
    """
    モデルマスターに登録されている全てのモデル情報を取得する。

    Args:
        conn (Connection): DBコネクション

    Returns:
        List[Dict]: モデルマスター情報のリスト
            - id: モデルID
            - model_name: モデル名
            - revision: モデルのリビジョン
            - class_name: このモデルを処理するクラス
            - screen_name: モデルの表示名
            - updated_at: レコードの更新日時
            - registed_at: レコードの登録日時
    """
    sql = "SELECT * FROM models"
    return conn.execute(sql).fetchall()


def get (conn:Connection, model_name:str, revision:str) -> Dict:
    """
    モデル名とリビジョンからモデルマスター情報を取得する。

    Args:
        conn (Connection): DBコネクション
        model_name (str): モデル名
        revision (str): リビジョン

    Returns:
        Dict: モデルマスター情報
            - id: モデルID
            - model_name: モデル名
            - revision: モデルのリビジョン
            - class_name: このモデルを処理するクラス
            - screen_name: モデルの表示名
            - updated_at: レコードの更新日時
            - registed_at: レコードの登録日時
    """
    sql = "SELECT * FROM models WHERE model_name = ? AND revision = ?"
    return conn.execute(sql, (model_name, revision,)).fetchone()


def is_exists (conn:Connection, model_name:str, revision:str) -> bool:
    """
    指定したモデル名とリビジョンのモデルが存在するか判定する。

    Args:
        conn (Connection): DBコネクション
        model_name (str): モデル名
        revision (str): リビジョン
    
    Returns:
        bool: True:存在する、False:存在しない
    """
    sql = "SELECT COUNT(*) FROM models WHERE model_name = ? and revision = ?"
    return conn.execute(sql, (model_name, revision)).fetchone()[0] > 0


def update (conn: Connection, model_name:str, revision:str, **kwargs) -> None:
    """
    モデル名とリビジョンからモデルマスター情報を更新する。

    Args:
        conn (Connection): DBコネクション
        model_name (str): モデル名
        revision (str): リビジョン
        **kwargs: 更新するカラム名と値
    
    Returns:
        None
    """
    sql = "UPDATE models SET "
    sql += ", ".join([f"{key} = ?" for key in kwargs.keys()])
    sql += "," if len(kwargs) > 0 else ""
    sql += " updated_at = CURRENT_TIMESTAMP"
    sql += " WHERE model_name = ? AND revision = ?"
    conn.execute(sql, (*kwargs.values(), model_name, revision))
    return


def delete (conn: Connection, model_name:str, revision:str) -> None:
    """
    モデル名とリビジョンからモデルマスター情報を削除する。

    Args:
        conn (Connection): DBコネクション
        model_name (str): モデル名
        revision (str): リビジョン
    """
    sql = "DELETE FROM models WHERE model_name = ? AND revision = ?"
    conn.execute(sql, (model_name, revision))
    return