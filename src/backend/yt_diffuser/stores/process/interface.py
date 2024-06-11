"""
プロセスストアのインターフェースを提供するモジュール
"""
from typing import Optional, Callable
from enum import Enum
from abc import ABCMeta, abstractmethod
import multiprocessing
from multiprocessing.context import SpawnContext, SpawnProcess

class ProcessKey(Enum):
    """
    プロセスキーを列挙する列挙型
    """
    GENERATOR = 'generator'
    DOWNLOADER = 'downloader'
    WEB = 'web'
    SELF = 'self'


class IProcessContextStore(metaclass=ABCMeta):
    """
    プロセスコンテキストストアのインターフェース
    """

    @abstractmethod
    def get_context(self) -> SpawnContext:
        """
        プロセスコンテキストを取得する。

        Returns:
            SpawnContext: プロセスコンテキスト
        """
        pass


class IProcessStore(metaclass=ABCMeta):
    """
    プロセスストアのインターフェース
    """
    
    def create_process(self, key:ProcessKey, target, args=(), kwargs={}) -> SpawnProcess:
        """
        プロセスデータを作成してストックする。
        同一キーが存在する場合は上書きする。

        Args:
            key (ProcessKey): プロセス名
            target (function): プロセスの実行関数
            args (tuple): 引数
            kwargs (dict): キーワード引数
        """
        pass

    def get_process(self, key:ProcessKey) -> Optional[SpawnProcess]:
        """
        プロセスデータを取得する。
        存在しない場合はNoneを返す。

        Args:
            key (ProcessKey): プロセス名

        Returns:
            ProcessData: プロセスデータ
        """
        pass

    def remove_process(self, key:ProcessKey):
        """
        プロセスデータを削除する。

        Args:
            key (ProcessKey): プロセス名
        """
        pass

    def remove_all_process(self):
        """
        全てのプロセスデータを削除する。
        """
        pass

class IProcessQueueStore(metaclass=ABCMeta):
    """
    プロセスキューストアのインターフェース
    """

    def get_queue(self, key:ProcessKey) -> Optional[multiprocessing.Queue]:
        """
        キューを取得する。
        存在しない場合はNoneを返す。

        Args:
            key (str): キー名

        Returns:
            Queue: キュー
        """
        pass

    def set_queue(self, key:ProcessKey, queue:multiprocessing.Queue):
        """
        キューを設定する。
        同一キーが存在する場合は上書きする。

        Args:
            key (str): キー名
            queue (Queue): キュー
        """
        pass

    def create_queue(self, key:ProcessKey) -> multiprocessing.Queue:
        """
        新規にキューを作成してストックする。
        同一キーが存在する場合は上書きする。

        Args:
            key (str): キュー名
        
        Returns:
            Queue: 作成したキュー
        """
        pass
    
    def set_self_queue(self, queue:multiprocessing.Queue):
        """
        自分自身のキューを設定する。

        Args:
            queue (Queue): キュー
        """
        pass
    
    def get_self_queue(self) -> multiprocessing.Queue:
        """
        自分自身のキューを取得する。
        存在しない場合は新規に作成する。

        Returns:
            Queue: キュー
        """
        pass

    def remove_queue(self, key:ProcessKey):
        """
        キューを削除する。

        Args:
            key (str): キュー名
        """
        pass
