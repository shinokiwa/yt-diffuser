"""
SQLite3 データベース接続モジュール

"""
from typing import List
from logging import getLogger; logger = getLogger(__name__)
import sqlite3
from pathlib import Path

from injector import inject, singleton

from .interface import IDBConnection, IDBCursor
from .utils import connect_database
from yt_diffuser.types.path import AppPath

@singleton
class DBConnection(IDBConnection):
    """
    SQLite3 データベース接続
    """
    
    @inject
    def __init__(self, pt:AppPath) -> None:
        """
        コンストラクタ
        """
        self.db_path:Path = pt.DB_FILE
        self.conn:sqlite3.Connection = None

    def connect(self) -> IDBConnection:
        """
        DBに接続する
        """
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = connect_database(self.db_path)
        return self

    def close(self) -> None:
        """
        DB接続を閉じる
        """
        if self.conn.in_transaction:
            self.conn.commit()

        self.conn.close()
        self.conn = None
    
    def execute(self, sql:str, params:tuple=()) -> 'IDBCursor':
        """
        SQLを実行する
        """
        cursor = self.conn.execute(sql, params)
        return DBCursor(cursor)
    
    def executescript(self, sql:str) -> 'IDBCursor':
        """
        複数のSQLを実行する
        """
        cursor = self.conn.executescript(sql)
        return DBCursor(cursor)

    def __enter__(self) -> IDBConnection:
        """
        コンテキストマネージャの開始処理
        """
        return self.connect()

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """
        コンテキストマネージャの終了処理
        """
        self.close()

class DBCursor(IDBCursor):
    """
    SQLite3 データベースカーソル
    抽象化のためのラッパー
    """

    def __init__(self, cursor:sqlite3.Cursor) -> None:
        """
        コンストラクタ
        """
        self.cursor = cursor

    def fetchone(self) -> dict:
        """
        1行取得する
        """
        row:sqlite3.Row = self.cursor.fetchone()
        return dict(row) if row is not None else None

    def fetchall(self) -> list:
        """
        全行取得する
        """
        rows:List[sqlite3.Row] = self.cursor.fetchall()
        return [dict(row) for row in rows]