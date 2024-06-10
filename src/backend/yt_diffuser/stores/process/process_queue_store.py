from typing import Optional, Dict
from logging import getLogger; logger = getLogger(__name__)
import multiprocessing

from injector import inject

from .interface import IProcessQueueStore, IProcessContextStore, ProcessKey

class ProcessQueueStore(IProcessQueueStore):
    """
    プロセスキューをストックするストアクラス
    """

    _queues: Dict[ProcessKey, multiprocessing.Queue] = {}
    """
    キューのストック

    プロセス名をキーにしてキューを格納する。
    """

    @inject
    def __init__(self, context_store:IProcessContextStore):
        """
        コンストラクタ

        Args:
            context_store (IProcessContextStore): コンテキストストア
        """
        self.context_store = context_store

    def create_queue(self, key: ProcessKey) -> multiprocessing.Queue:
        """
        新規にキューを作成してストックする。
        同一キーが存在する場合は上書きする。

        Args:
            key (str): キュー名
        
        Returns:
            Queue: 作成したキュー
        """
        context = self.context_store.get_context()
        queue = context.Queue()
        self.set_queue(key, queue)
        return queue
    
    def set_queue(self, key: ProcessKey, queue: multiprocessing.Queue):
        """
        キューを設定する。
        同一キーが存在する場合は上書きする。

        Args:
            key (str): キー名
            queue (Queue): キュー
        """
        self.__class__._queues[key] = queue
    
    def get_queue(self, key: ProcessKey) -> Optional[multiprocessing.Queue]:
        """
        キューを取得する。
        存在しない場合はNoneを返す。

        Args:
            key (str): キー名

        Returns:
            Queue: キュー
        """
        return self.__class__._queues.get(key, None)
    
    def set_self_queue(self, queue: multiprocessing.Queue):
        """
        自分自身のキューを設定する。

        Args:
            queue (Queue): キュー
        """
        self.set_queue(ProcessKey.SELF, queue)
    
    def get_self_queue(self) -> multiprocessing.Queue:
        """
        自分自身のキューを取得する。
        存在しない場合は新規に作成する。

        Returns:
            Queue: キュー
        """
        return self.get_queue(ProcessKey.SELF) or self.create_queue(ProcessKey.SELF)
    
    def remove_queue(cls, key:ProcessKey) -> None:
        """
        キューを削除する。

        Args:
            key (str): キュー名
        """
        cls.__class__._queues.pop(key, None)

