import multiprocessing
from queue import Queue

from injector import inject

from yt_diffuser.types.generator.message import GenerateMessage, GeneratorCommand
from yt_diffuser.types.error import GeneratorExitSignal
from yt_diffuser.stores.generator.interface import IGeneratorStatusStore

class ListenUsecase:
    """
    生成プロセスリスナーのユースケース
    """

    @inject
    def __init__(
        self,
        store:IGeneratorStatusStore
    ):
        self.store = store


    def handle(self, recv_queue:multiprocessing.Queue, task_queue:Queue):
        """
        リスナーの処理を実行する
        """
        recv_data = recv_queue.get()
        message = GenerateMessage(**recv_data)

        # ストップシグナルの有効化
        if message.command == GeneratorCommand.EXIT or message.command == GeneratorCommand.STOP:
            self.store.state.stop_signal = True

        task_queue.put(message)

        # 終了シグナルの有効化
        if message.command == GeneratorCommand.EXIT:
            self.store.state.exit_signal = True
            raise GeneratorExitSignal()