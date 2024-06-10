"""
yt_diffuser.stores.database.connection

SQLite3 データベース接続モジュール
"""
import pytest

import sqlite3

from injector import Injector

from specs.unit.injector import TestInjectModule

from yt_diffuser.stores.database.connection import *

class TestDBConnection:
    """
    DBConnection

    SQLite3 データベース接続
    """

    def test_connect_and_close(self):
        """
        connect

        it:
            - DBに接続する
        
        close

        it:
            - DB接続を閉じる
        """
        injector = Injector([TestInjectModule()])
        db = injector.get(DBConnection)

        assert isinstance(db.connect().conn, sqlite3.Connection), "コネクションが取得できる。"

        db.close()
        assert db.conn is None, "コネクションが閉じられている。"

    def test_enter_and_exit(self):
        """
        __enter__

        it:
            - コンテキストマネージャの開始処理

        __exit__

        it:
            - コンテキストマネージャの終了処理
        """
        injector = Injector([TestInjectModule()])
        db = injector.get(DBConnection)

        assert db.__enter__() == db, "自分自身を返す。"
        assert isinstance(db.conn, sqlite3.Connection), "コネクションが取得できる。"

        db.__exit__(None, None, None)
        assert db.conn is None, "コネクションが閉じられている。"

    def test_execute(self):
        """
        execute

        it:
            - SQLを実行する
        """
        injector = Injector([TestInjectModule()])
        db = injector.get(DBConnection)

        with db:
            cursor = db.execute("SELECT 1")
            assert isinstance(cursor, DBCursor), "カーソルが取得できる。"
    
    def test_executescript(self):
        """
        executescript

        it:
            - 複数のSQLを実行する
        """
        injector = Injector([TestInjectModule()])
        db = injector.get(DBConnection)

        with db:
            cursor = db.executescript("SELECT 1; SELECT 2")
            assert isinstance(cursor, DBCursor), "カーソルが取得できる。"


class TestDBCursor:
    """
    DBCursor

    SQLite3 データベースカーソル
    """

    def test_fetchone(self):
        """
        fetchone

        it:
            - 1行取得する
        """
        injector = Injector([TestInjectModule()])
        db = injector.get(DBConnection)

        with db:
            cursor = db.execute("SELECT 1 AS id")
            assert cursor.fetchone() == {"id": 1}, "1行取得できる。"

    def test_fetchall(self):
        """
        fetchall

        it:
            - 全行取得する
        """
        injector = Injector([TestInjectModule()])
        db = injector.get(DBConnection)

        with db:
            cursor = db.execute("SELECT 1 AS id UNION SELECT 2 AS id")
            assert cursor.fetchall() == [
                {"id": 1},
                {"id": 2}
            ], "全行取得できる。"
