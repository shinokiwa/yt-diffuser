from abc import ABCMeta, abstractmethod
from enum import Enum
from threading import Thread

class ThreadKeys(Enum):
    """
    スレッドキーを列挙する列挙型
    """
    GENERATOR = 'generator'

class IThreadStore(metaclass=ABCMeta):
    """
    スレッドストアのインターフェース

    一応複数のスレッドを管理できるようになっているが、
    現実的には1つのスレッドしか使わないと思われる。
    """

    @abstractmethod
    def create_thread(self, key:str, target, args=(), kwargs={}) -> Thread:
        """
        スレッドデータを作成してストックする。
        同一キーが存在する場合は上書きする。

        Args:
            key (str): スレッド名
            target (function): スレッドの実行関数
            args (tuple): 引数
            kwargs (dict): キーワード引数
        """
        pass

    @abstractmethod
    def get_thread(self, key:str):
        """
        スレッドデータを取得する。
        存在しない場合はNoneを返す。

        Args:
            key (str): スレッド名

        Returns:
            ThreadData: スレッドデータ
        """
        pass

    @abstractmethod
    def is_alive(self, key:str) -> bool:
        """
        スレッドが生存しているかどうかを返す。

        Args:
            key (str): スレッド名

        Returns:
            bool: 生存しているかどうか
        """
        pass
