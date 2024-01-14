"""
モデル情報テーブル model_info
"""
from typing import Dict, List
from sqlite3 import Connection

from yt_diffuser.store.enums import ModelClass

def create_table (conn:Connection) -> None:
    """
    テーブルを作成する。

    Args:
        conn (Connection): DBコネクション
    """
    conn.executescript((
        "CREATE TABLE model_info ("
            "model_name      TEXT        NOT NULL,"                              # モデル名
            "class_name      TEXT        NOT NULL,"                              # このモデルを処理するクラス
            "screen_name     TEXT,"                                              # モデルの表示名
            "updated_at      DATETIME    NOT NULL    DEFAULT CURRENT_TIMESTAMP," # モデルの更新日時
            "registed_at     DATETIME    NOT NULL    DEFAULT CURRENT_TIMESTAMP,"  # モデルの登録日時
            "PRIMARY KEY (model_name)"
        ");"
        # インデックス
        "CREATE INDEX model_info_class ON model_info (class_name);"
    ))

def save (conn:Connection, model_name:str, class_name:ModelClass, screen_name:str = "") -> None:
    """
    モデル情報を保存する。

    - レコードが存在する場合は更新、存在しない場合は追加する。

    Args:
        conn (Connection): DBコネクション
        model_name (str): モデル名
        class_name (ModelClass): このモデルを処理するクラス名
        screen_name (str): モデルの表示名
    
    Returns:
        None
    """
    sql = (
        "INSERT INTO model_info (model_name, class_name, screen_name)"
        " VALUES (?, ?, ?)"
        " ON CONFLICT(model_name)"
        " DO UPDATE SET class_name = excluded.class_name, screen_name = excluded.screen_name"
    )
    conn.execute(sql, (model_name, class_name.value, screen_name))
    return


def get (conn:Connection, model_name:str) -> Dict:
    """
    モデル名からモデル情報を取得する。

    Args:
        conn (Connection): DBコネクション
        model_name (str): モデル名

    Returns:
        Dict: モデルマスター情報
            - model_name: モデル名
            - class_name: このモデルを処理するクラス
            - screen_name: モデルの表示名
            - updated_at: レコードの更新日時
            - registed_at: レコードの登録日時
    """
    sql = "SELECT * FROM model_info WHERE model_name = ?"
    result = conn.execute(sql, (model_name, )).fetchone()
    return result


def delete (conn: Connection, model_name:str) -> None:
    """
    モデル情報を削除する。

    Args:
        conn (Connection): DBコネクション
        model_name (str): モデル名
    """
    sql = "DELETE FROM model_info WHERE model_name = ?"
    conn.execute(sql, (model_name,))
    return