from typing import Dict
import json

from injector import inject

from yt_diffuser.stores.database.store.interface import IDBStore, IDBConnection

class FormUseCase:
    """
    最新のフォーム情報を管理するユースケース
    """

    @inject
    def __init__(self, conn:IDBConnection, db:IDBStore):
        """
        コンストラクタ
        
        Args:
            conn (IDBConnection): DBコネクション
            db (IDBStore): DBストア
        """
        self.conn = conn
        self.db = db

    def read(self) -> Dict:
        """
        最新のフォーム情報を取得する

        Returns:
            Dict : フォーム情報
        """

        with self.conn:
            form = self.db.read("api/form", b"{}")
            data = json.loads(form)

        return data

    def write(self, data:Dict):
        """
        最新のフォーム情報を保存する
        """

        with self.conn:
            self.db.write("api/form", json.dumps(data))
