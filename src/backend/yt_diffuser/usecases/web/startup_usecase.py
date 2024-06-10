"""
スタートアップ処理のユースケース
"""
from injector import inject

from yt_diffuser.stores.database.store.interface import IDBStore, IDBConnection

class StartUpUseCase():
    """
    スタートアップ処理
    """

    @inject
    def __init__(self, conn:IDBConnection, store:IDBStore):
        """
        コンストラクタ

        Args:
            conn (IDBConnection): DBコネクション
            store (IDBStore): DBストア
        """
        self.conn = conn
        self.store = store
    
    def startup(self):
        """
        スタートアップ処理
        """
        with self.conn:
            self.store.create_table()
