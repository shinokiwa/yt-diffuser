from typing import Dict
from logging import getLogger; logger = getLogger(__name__)
import atexit
from multiprocessing.context import SpawnProcess

from injector import inject

from .interface import IProcessStore, IProcessContextStore, ProcessKey

class ProcessStore(IProcessStore):
    """
    プロセスをストックするストアクラス
    """

    _processes: Dict[ProcessKey, SpawnProcess] = {}
    """
    プロセスのストック
    プロセス名をキーにしてプロセスデータを格納する。
    """

    @inject
    def __init__(self, context_store:IProcessContextStore):
        """
        コンストラクタ

        Args:
            context_store (IProcessContextStore): コンテキストストア
        """
        self.context_store = context_store

    def create_process(self, key:ProcessKey, target, args=(), kwargs={}) -> SpawnProcess:
        """
        新規にプロセスを作成してストックする。
        同一キーが存在する場合は上書きする。

        Args:
            key (ProcessKey): プロセス名
            target (function): プロセスの実行関数
            args (tuple): 引数
            kwargs (dict): キーワード引数

        Returns:
            ProcessData: 作成したプロセスデータ
        """
        process = self.context_store.get_context().Process(target=target, args=args, kwargs=kwargs)
        self.__class__._processes[key] = process
        return process
    
    def get_process(self, key:ProcessKey) -> SpawnProcess:
        """
        プロセスデータを取得する。

        Args:
            key (ProcessKey): プロセス名

        Returns:
            ProcessData: プロセスデータ
        """
        return self.__class__._processes.get(key, None)
    
    def remove_process(self, key:ProcessKey) -> None:
        """
        プロセスデータを削除する。

        Args:
            key (ProcessKey): プロセス名
        """
        process = self.get_process(key)
        if process is not None and process.is_alive():
            process.join(timeout=30)
            process.terminate()

        self.__class__._processes.pop(key, None)
    
    @classmethod
    def remove_all_processes(cls) -> None:
        """
        全てのプロセスデータを削除する。
        """
        for key, process in cls._processes.items():
            if process.is_alive():
                process.join(timeout=30)
                process.terminate()
        cls._processes.clear()
            

atexit.register(ProcessStore.remove_all_processes)
