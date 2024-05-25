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
        Dict: フォーム名 : フォーム値 の形式の辞書
    """
    sql = "SELECT name, value FROM form_data"
    data = conn.execute(sql).fetchall()

    result = {}
    for r in data:
        result[r['name']] = r['value']
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

def delete_not_in (conn:Connection, names:List[str]) -> None:
    """
    指定したフォーム名以外のフォーム情報を削除する。

    Args:
        conn (Connection): DBコネクション
        names (List[str]): 保持するフォーム名のリスト
    
    Returns:
        None
    """
    sql = "DELETE FROM form_data WHERE name NOT IN ({})".format(",".join(["?" for _ in names]))
    conn.execute(sql, names)
    return