"""
yt_diffuser.stores.database.store
"""
import pytest

from injector import Injector

from specs.unit.injector import TestInjectModule

from yt_diffuser.stores.database.store.store import DBStore

class TestDBStore:
    """
    DBStore

    SQLite3 データベースストア
    """

    def test_create_table(self):
        """
        create_table

        it:
            - テーブルを作成する
        """
        injector = Injector([TestInjectModule()])
        db = injector.get(DBStore)

        with db.connection() as conn:
            db.create_table()

            cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='store'")
            assert cursor.fetchone()['name'] == "store", "テーブルを作成する。"


    def test_read(self):
        """
        read

        it:
            - ストアからデータを読み込む
        """
        injector = Injector([TestInjectModule()])
        db = injector.get(DBStore)

        with db.connection() as conn:
            db.create_table()
            conn.execute("INSERT INTO store (key, data) VALUES (?, ?)", ("api/form", b"{}"))

            assert db.read("api/form", b"{}") == b"{}", "データを読み込む。"

    def test_write(self):
        """
        write

        it:
            - ストアにデータを書き込む
        """
        injector = Injector([TestInjectModule()])
        db = injector.get(DBStore)

        with db.connection() as conn:
            db.create_table()
            db.write("api/form", b"{}")

            cursor = conn.execute("SELECT data FROM store WHERE key=?", ("api/form",))
            assert cursor.fetchone()['data'] == b"{}", "データを書き込む。"

            db.write("api/form", b'{"key":"value"}')

            cursor = conn.execute("SELECT data FROM store WHERE key=?", ("api/form",))
            assert cursor.fetchone()['data'] == b'{"key":"value"}', "データを更新する。"

    def test_delete(self):
        """
        delete

        it:
            - ストアからデータを削除する
        """
        injector = Injector([TestInjectModule()])
        db = injector.get(DBStore)

        with db.connection() as conn:
            db.create_table()
            conn.execute("INSERT INTO store (key, data) VALUES (?, ?)", ("api/form", b"{}"))

            db.delete("api/form")

            cursor = conn.execute("SELECT data FROM store WHERE key=?", ("api/form",))
            assert cursor.fetchone() is None, "データを削除する。"
    
