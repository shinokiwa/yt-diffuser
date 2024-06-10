"""
DBストアのインターフェース
"""
from abc import ABCMeta, abstractmethod

from ..interface import IDBConnection

class IDBStore(metaclass=ABCMeta):
    """
    DBストアのインターフェース
    """

    @abstractmethod
    def connection(self) -> IDBConnection:
        """
        DB接続を取得する
        """
        pass

    @abstractmethod
    def create_table(self):
        """
        テーブルを作成する
        """
        pass

    @abstractmethod
    def read(self, key:str, default:bytes) -> bytes:
        """
        ストアからデータを読み込む

        Args:
            key (str): キー
            default (bytes): デフォルト値

        Returns:
            bytes : データ
        """
        pass

    @abstractmethod
    def write(self, key:str, data:bytes):
        """
        ストアにデータを書き込む

        Args:
            key (str): キー
            data (bytes): データ
        """
        pass

    @abstractmethod
    def delete(self, key:str):
        """
        ストアからデータを削除する

        Args:
            key (str): キー
        """
        pass