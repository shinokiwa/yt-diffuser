import multiprocessing
from threading import Thread
from queue import Queue

from injector import inject

from yt_diffuser.stores.process.interface import ProcessKey, IProcessQueueStore
from yt_diffuser.adapters.generator.interface import IGeneratorController, IGenerator, IGeneratorPresenter

class GeneratorStartupUsecase:
    """
    生成処理プロセスの起動ユースケース
    """

    @inject
    def __init__(
        self,
        controller:IGeneratorController,
        generator:IGenerator,
        presenter:IGeneratorPresenter
    ):
        self.controller = controller
        self.generator = generator
        self.presenter = presenter

    def execute(self, send_queue:multiprocessing.Queue, recv_queue:multiprocessing.Queue):
        """
        生成処理プロセスの起動
        """

        # スレッド用のタスクキュー、メッセージキューを作成
        task_queue = Queue()
        result_queue = Queue()

        # コントローラーをスレッドで起動
        controller = Thread(target=self.controller.listen, args=(recv_queue, task_queue))
        controller.start()

        # ジェネレーターをスレッドで起動
        generator = Thread(target=self.generator.process, args=(task_queue, result_queue))
        generator.start()

        # プレゼンターをスレッドで起動
        presenter = Thread(target=self.presenter.send, args=(result_queue, send_queue))
        presenter.start()

        controller.join()
        generator.join()
        presenter.join()
        return