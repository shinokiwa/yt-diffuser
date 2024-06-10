from typing import List, Dict
from abc import ABCMeta, abstractmethod

class IDBConnection(metaclass=ABCMeta):
    """
    DB接続のインターフェース
    """

    @abstractmethod
    def connect(self) -> 'IDBConnection':
        """
        DBに接続する
        """
        pass

    @abstractmethod
    def close(self):
        """
        DB接続を閉じる
        """
        pass

    @abstractmethod
    def execute(self, sql:str, params:tuple) -> 'IDBCursor':
        """
        SQLを実行する
        """
        pass
    
    @abstractmethod
    def executescript(self, sql:str) -> 'IDBCursor':
        """
        複数のSQLを実行する
        """
        pass

    @abstractmethod
    def __enter__(self) -> 'IDBConnection':
        """
        コンテキストマネージャの開始処理
        """
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_value, traceback):
        """
        コンテキストマネージャの終了処理
        """
        pass


class IDBCursor(metaclass=ABCMeta):
    """
    DBカーソルのインターフェース
    """

    @abstractmethod
    def fetchone(self) -> Dict:
        """
        1行取得する
        """
        pass

    @abstractmethod
    def fetchall(self) -> List[Dict]:
        """
        全行取得する
        """
        pass
