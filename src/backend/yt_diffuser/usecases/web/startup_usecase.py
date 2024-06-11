import logging; logger = logging.getLogger(__name__)

from injector import inject

from yt_diffuser.stores.database.store.interface import IDBStore, IDBConnection
from yt_diffuser.stores.process.interface import IProcessStore

class StartUpUseCase():
    """
    スタートアップ処理
    """

    @inject
    def __init__(self, conn:IDBConnection, db_store:IDBStore, process:IProcessStore):
        """
        コンストラクタ

        Args:
            conn (IDBConnection): DBコネクション
            store (IDBStore): DBストア
        """
        self.conn = conn
        self.db_store = db_store
        self.process = process
    
    def startup(self):
        """
        スタートアップ処理
        """
        logger.debug("startup")
        with self.conn:
            self.db_store.create_table()
    
    def shutdown(self):
        """
        シャットダウン処理
        """
        logger.debug("shutdown")
        self.process.remove_all_process()
