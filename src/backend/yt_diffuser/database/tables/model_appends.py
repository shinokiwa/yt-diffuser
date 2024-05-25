"""
モデル追加情報テーブル model_appends
キーバリュー形式。
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
        "CREATE TABLE model_appends ("
            "model_name      TEXT        NOT NULL,"                              # モデル名
            "key             TEXT        NOT NULL,"                              # キー
            "value           TEXT        NOT NULL,"                              # 値
            "updated_at      DATETIME    NOT NULL    DEFAULT CURRENT_TIMESTAMP," # モデルの更新日時
            "registed_at     DATETIME    NOT NULL    DEFAULT CURRENT_TIMESTAMP,"  # モデルの登録日時
            "PRIMARY KEY (model_name, key)"
        ");"
    ))


def save (conn:Connection, model_name:str, key:str, value:str) -> None:
    """
    モデル追加情報を保存する。

    - レコードが存在する場合は更新、存在しない場合は追加する。

    Args:
        conn (Connection): DBコネクション
        model_name (str): モデル名
        key (str): キー
        value (str): 値

    Returns:
        None
    """
    sql = (
        "INSERT INTO model_appends (model_name, key, value)"
        " VALUES (?, ?, ?)"
        " ON CONFLICT(model_name, key)"
        " DO UPDATE SET value = excluded.value"
    )
    conn.execute(sql, (model_name, key, value))
    return


def get (conn:Connection, model_name:str) -> Dict:
    """
    モデル名からモデル追加情報を取得する。

    Args:
        conn (Connection): DBコネクション
        model_name (str): モデル名

    Returns:
        Dict: キーと値のペアのリスト
    """
    sql = (
        "SELECT * FROM model_appends"
        " WHERE model_name = ?"
    )
    rows = conn.execute(sql, (model_name,)).fetchall()

    return {row["key"]: row["value"] for row in rows}


def delete (conn:Connection, model_name:str, key:str) -> None:
    """
    モデル追加情報を削除する。

    Args:
        conn (Connection): DBコネクション
        model_name (str): モデル名
        key (str): キー

    Returns:
        None
    """
    sql = (
        "DELETE FROM model_appends"
        " WHERE model_name = ?"
        " AND key = ?"
    )
    conn.execute(sql, (model_name, key))
    return


def delete_all (conn:Connection, model_name:str) -> None:
    """
    モデル追加情報を削除する。

    Args:
        conn (Connection): DBコネクション
        model_name (str): モデル名

    Returns:
        None
    """
    sql = (
        "DELETE FROM model_appends"
        " WHERE model_name = ?"
    )
    conn.execute(sql, (model_name,))
    return
