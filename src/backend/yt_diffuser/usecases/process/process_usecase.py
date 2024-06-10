import logging; logger = logging.getLogger(__name__)

from injector import inject

from yt_diffuser.stores.process.interface import IProcessQueueStore, IProcessStore, ProcessKey
from yt_diffuser.types.error import DuplicateProcessError

from yt_diffuser.adapters.generator.main import generator_main


class ProcessUseCase:
    """
    プロセスを管理するユースケース
    """

    @inject
    def __init__(self, process_store:IProcessStore, queue_store:IProcessQueueStore):
        """
        コンストラクタ
        
        Args:
            process_store (IProcessStore): プロセスストア
            queue_store (IProcessQueueStore): キューストア
        """
        self.process_store = process_store
        self.queue_store = queue_store

    def is_running(self, key:ProcessKey) -> bool:
        """
        サブプロセスが動作中かどうかを返す。

        Returns:
            bool: サブプロセスが実行中の場合はTrue
        """
        process = self.process_store.get_process(key)
        return process is not None and process.is_alive()


    def run(self, key:ProcessKey) -> None:
        """
        サブプロセスを起動する。
        """
        if self.is_running(key):
            raise DuplicateProcessError(key) 

        recv_queue = self.queue_store.get_self_queue()
        send_queue = self.queue_store.create_queue(key)

        logger.debug("generator process load")

        process = self.process_store.create_process(key,
                                                    target=generator_main,
                                                    args=(recv_queue, send_queue)
                                                    )

        logger.debug("generator process start")

        process.start()
        return

    def terminate(self, key:ProcessKey) -> None:
        """
        サブプロセスを終了する。

        停止状態のプロセスを終了してもエラーにならない。
        """
        self.process_store.remove_process(key)
        self.queue_store.remove_queue(key)
            
    
    def get_send_queue(self, key:ProcessKey):
        """
        サブプロセスに送信するキューを取得する。

        Args:
            key (ProcessKey): プロセスのキー
        """
        return self.queue_store.get_queue(key)
