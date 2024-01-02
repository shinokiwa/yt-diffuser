"""
form_data
フォームの最新状態を保存するテーブル
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
        "CREATE TABLE form_data ("
            "name            TEXT        NOT NULL,"                              # モデル名
            "value           TEXT        NOT NULL,"                              # モデルのリビジョン
            "updated_at      DATETIME    NOT NULL    DEFAULT CURRENT_TIMESTAMP," # モデルの更新日時
            "registed_at     DATETIME    NOT NULL    DEFAULT CURRENT_TIMESTAMP,"  # モデルの登録日時
            "PRIMARY KEY (name)"
        ");"
    ))

def save (conn:Connection, **kwargs) -> None:
    """
    フォーム情報を保存する。

    - レコードが存在する場合は更新、存在しない場合は追加する。
    - 指定した辞書のキーと値を保存する。

    Args:
        conn (Connection): DBコネクション
        **kwargs: 保存するキーと値
    
    Returns:
        None
    """
    sql = (
        "INSERT INTO form_data (name, value)"
        " VALUES"
    )

    sql += ",".join(["(?, ?)" for _ in kwargs])

    sql += (
        " ON CONFLICT(name)"
        " DO UPDATE SET value = excluded.value, updated_at = CURRENT_TIMESTAMP"
    )
    values = []
    for key, value in kwargs.items():
        values.append(key)
        values.append(value)

    conn.execute(sql, values)
    return


def get_all (conn:Connection) -> List[Dict]:
    """
    フォーム情報を全て取得する。

    Args:
        conn (Connection): DBコネクション

    Returns:
        Dict: フォーム最新情報
            - name: フォーム名
            - value: フォームの値
            - updated_at: レコードの更新日時
            - registed_at: レコードの登録日時
    """
    sql = "SELECT * FROM form_data"
    result = conn.execute(sql).fetchall()
    return result

def delete (conn:Connection, name:str) -> None:
    """
    フォーム情報を削除する。

    Args:
        conn (Connection): DBコネクション
        name (str): 削除するフォーム名
    
    Returns:
        None
    """
    sql = "DELETE FROM form_data WHERE name = ?"
    conn.execute(sql, (name,))
    return