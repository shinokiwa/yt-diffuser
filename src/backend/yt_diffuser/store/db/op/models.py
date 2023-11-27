""" モデル情報マスター models のテーブル操作モジュール
"""
from typing import Dict
from sqlite3 import Connection

def create_table (conn:Connection) -> None:
    """ テーブルを作成
    """
    conn.executescript((
        "CREATE TABLE models ("
            "id              INTEGER     NOT NULL    PRIMARY KEY AUTOINCREMENT," # モデルID
            "path_name       TEXT        NOT NULL,"                              # モデルのパス
            "name            TEXT        NOT NULL,"                              # モデルの名前
            "revision        TEXT        NOT NULL,"                              # モデルのリビジョン
            "class_name      INT         NOT NULL,"                              # このモデルを処理するクラス
            "updated_at      DATETIME    NOT NULL    DEFAULT CURRENT_TIMESTAMP," # モデルの更新日時
            "registed_at     DATETIME    NOT NULL    DEFAULT CURRENT_TIMESTAMP"  # モデルの登録日時
        ");"
        # インデックス
        "CREATE UNIQUE INDEX models_path_name ON models (path_name);"
        "CREATE INDEX models_name ON models (name);"
        "CREATE INDEX models_revision ON models (revision);"
        "CREATE INDEX models_class ON models (class_name);"
    ))


def insert (conn:Connection, path_name:str, name:str, revision:str, class_name:str) -> None:
    """ モデルマスターにモデル情報を挿入
    """
    sql = "INSERT INTO models (path_name, name, revision, class_name) VALUES (?, ?, ?, ?)"
    conn.execute(sql, (path_name, name, revision, class_name))
    return


def get_by_pathname (conn:Connection, path_name:str) -> Dict:
    """ パス名からモデルマスター情報を取得

    Args:
        conn (Connection): DBコネクション
        path_name (str): パス名

    Returns:
        Dict: モデルマスター情報
            - id: モデルID
            - path_name: モデルのパス
            - name: モデルの名前
            - revision: モデルのリビジョン
            - class_name: このモデルを処理するクラス
    """
    sql = "SELECT id, path_name, name, revision, class_name FROM models WHERE path_name = ?"
    return conn.execute(sql, (path_name,)).fetchone()


def is_exists_by_pathname (conn:Connection, path_name:str) -> bool:
    """ 指定したパス名のモデルが存在するか判定
    """
    sql = "SELECT COUNT(*) FROM models WHERE path_name = ?"
    return conn.execute(sql, (path_name,)).fetchone()[0] > 0


def update_by_pathname (conn: Connection, path_name:str, **kwargs) -> None:
    """ パス名からモデルマスター情報を更新
    """
    sql = "UPDATE models SET "
    sql += ", ".join([f"{key} = ?" for key in kwargs.keys()])
    sql += " WHERE path_name = ?"
    conn.execute(sql, (*kwargs.values(), path_name))
    return


def delete_by_pathname (conn: Connection, pathname:str) -> None:
    """ パス名からモデルマスター情報を削除
    """
    sql = "DELETE FROM models WHERE path_name = ?"
    conn.execute(sql, (pathname,))
    return