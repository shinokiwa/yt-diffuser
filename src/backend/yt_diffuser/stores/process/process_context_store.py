from logging import getLogger; logger = getLogger(__name__)
import multiprocessing
from multiprocessing.context import SpawnContext, SpawnProcess

from .interface import IProcessContextStore

class ProcessContextStore(IProcessContextStore):
    """
    プロセスコンテキストストア
    """

    _context = multiprocessing.get_context('spawn')
    """
    spawnプロセスのコンテキスト
    """

    def __init__(self):
        pass
    
    def get_context(self) -> SpawnContext:
        """
        プロセスコンテキストを取得する。

        Returns:
            SpawnContext: プロセスコンテキスト
        """
        return self.__class__._context
