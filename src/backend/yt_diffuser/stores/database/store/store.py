from logging import getLogger; logger = getLogger(__name__)

from injector import inject

from .interface import IDBStore, IDBConnection

class DBStore(IDBStore):
    """
    SQLite3 ストアテーブル操作
    """

    @inject
    def __init__(self, db:IDBConnection) -> None:
        """
        コンストラクタ
        """
        self.db:IDBConnection = db
    
    def connection(self) -> IDBConnection:
        return self.db
    
    def create_table(self):
        """
        テーブルを作成する。
        """
        self.db.executescript("""
            CREATE TABLE IF NOT EXISTS store (
                key TEXT PRIMARY KEY NOT NULL,
                data BLOB NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT (DATETIME('now', 'localtime')),
                update_at TIMESTAMP NOT NULL DEFAULT (DATETIME('now', 'localtime'))
            )
        """)

    def write(self, key:str, data:bytes):
        """
        データをストアに保存する。
        コミットはしないので、呼び出し元で行うこと。

        Args:
            key : str : キー
            data : bytes : データ
        """
        self.db.execute("""
            INSERT INTO store
                (key, data) VALUES (?, ?)
            ON CONFLICT(key) DO UPDATE
                SET data=excluded.data, update_at=DATETIME('now', 'localtime')
        """, (key, data))

    def read(self, key:str, default:bytes=None) -> bytes:
        """
        ストアからデータを取得する。

        Args:
            key : str : キー

        Returns:
            bytes : データ
        """
        cursor = self.db.execute("""
            SELECT data FROM store WHERE key=?
        """, (key,))
        row = cursor.fetchone()
        if row is None:
            return default
        return row["data"]

    def delete(self, key:str):
        """
        ストアからデータを削除する。
        コミットはしないので、呼び出し元で行うこと。

        Args:
            conn : sqlite3.Connection : DB接続
            key : str : キー
        """
        self.db.execute("""
            DELETE FROM store WHERE key=?
        """, (key,))