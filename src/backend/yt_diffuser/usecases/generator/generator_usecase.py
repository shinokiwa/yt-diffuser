import logging; logger = logging.getLogger(__name__)
from queue import Queue

from injector import inject

from yt_diffuser.types.error import GeneratorExitSignal
from yt_diffuser.stores.generator.interface import IGeneratorStatusStore
from .load_usecase import GeneratorLoadUseCase
from .dispatch_usecase import GeneratorDispatchUseCase
from yt_diffuser.types.generator.message import (
    GenerateMessage,
    GeneratorCommand,
    GenerateMessageResult,
    GeneratorStatus
)

class GeneratorUseCase:
    """
    パイプラインを読み込むユースケース
    """

    @inject
    def __init__(
        self,
        store:IGeneratorStatusStore,
        loader:GeneratorLoadUseCase,
        dispatcher:GeneratorDispatchUseCase
    ):
        """
        コンストラクタ

        Args:
            path (AppPath): パス設定
            store (IGeneratorStatusStore): ステータスストア
            loader (GeneratorLoadUseCase): ロードユースケース
            dispatcher (GeneratorDispatchUseCase): ディスパッチユースケース
        """
        self.store = store
        self.loader = loader
        self.dispatcher = dispatcher
    
    def handle(self, task_queue:Queue, result_queue:Queue) -> None:
        """
        タスクを処理する
        """
        try:
            # 通常、停止シグナルが出る時はタスクキューにも値が入るが、念の為30秒おきにチェックする
            task:GenerateMessage = task_queue.get(timeout=30)

            # コントローラーが停止シグナルを出している場合は処理しない
            if self.store.state.stop_signal == False:
                if task.command == GeneratorCommand.LOAD:

                    self.loader.load(task, result_queue)
                
                elif task.command == GeneratorCommand.TEXT_TO_IMAGE:

                    self.dispatcher.dispatch(task, result_queue)

            # タスクキューがなくなった場合はカウントをリセットする            
            if task_queue.empty():
                self.store.reset_count()
                self.store.state.stop_signal = False
                result_queue.put(GenerateMessageResult(
                    status=GeneratorStatus.COMPLETED,
                ))

        except TimeoutError:
            pass
        
        # 終了シグナルが有効化されている場合は終了する
        if self.store.state.exit_signal == True:
            result_queue.put(GenerateMessageResult(
                status=GeneratorStatus.EXIT,
            ))

            raise GeneratorExitSignal()
