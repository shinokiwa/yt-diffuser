"""
prompt_archive
プロンプトの記録
"""
from typing import Dict, List
from enum import Enum
from sqlite3 import Connection

class Types(Enum):
    """
    typeの種別
    """
    PROMPT = "p"
    NEGATIVE_PROMPT = "n"

def create_table (conn:Connection) -> None:
    """
    テーブルを作成する。

    Args:
        conn (Connection): DBコネクション
    """
    conn.executescript((
        "CREATE TABLE prompt_archive ("
            "id              INTEGER     NOT NULL    PRIMARY KEY AUTOINCREMENT,"    # ID
            "type            TEXT        NOT NULL,"                                 # 種別 p:プロンプト n:ネガティブプロンプト
            "prompt          TEXT        NOT NULL,"                                 # プロンプト
            "updated_at      DATETIME    NOT NULL    DEFAULT CURRENT_TIMESTAMP,"    # 更新日時
            "registed_at     DATETIME    NOT NULL    DEFAULT CURRENT_TIMESTAMP"     # 登録日時
        ");"
    ))

def insert (conn:Connection, type:Types, prompt:str) -> None:
    """
    プロンプト記録を追加する。

    Args:
        conn (Connection): DBコネクション
        type (Types): 種別 Types
        prompt (str): プロンプト
    
    Returns:
        None
    """
    sql = (
        "INSERT INTO prompt_archive (type, prompt)"
        " VALUES (?, ?)"
    )
    conn.execute(sql, (type.value, prompt,))
    return


def get_by_type (conn:Connection, type:Types) -> List[Dict]:
    """
    指定した種別のプロンプト記録を取得する。

    Args:
        conn (Connection): DBコネクション
        type (Types): 種別 Types

    Returns:
        List[Dict]: プロンプト記録
            - id: ID
            - prompt: プロンプト
            - type: 種別 Types
            - updated_at: レコードの更新日時
            - registed_at: レコードの登録日時
    """
    sql = (
        "SELECT * FROM prompt_archive"
        " WHERE type = ?"
        " ORDER BY updated_at DESC, id DESC"
    )
    result = conn.execute(sql, (type.value,)).fetchall()
    return result

def update(conn:Connection, id:int) -> None:
    """
    プロンプト記録を更新する。
    今のところは最終更新日時を更新するだけ。

    Args:
        conn (Connection): DBコネクション
        id (int): ID
    
    Returns:
        None
    """
    sql = (
        "UPDATE prompt_archive"
        " SET updated_at = CURRENT_TIMESTAMP"
        " WHERE id = ?"
    )
    conn.execute(sql, (id,))
    return

def delete (conn:Connection, id:int) -> None:
    """
    プロンプト記録を削除する。

    Args:
        conn (Connection): DBコネクション
        id (int): 削除するID
    
    Returns:
        None
    """
    sql = "DELETE FROM prompt_archive WHERE id = ?"
    conn.execute(sql, (id,))
    return
