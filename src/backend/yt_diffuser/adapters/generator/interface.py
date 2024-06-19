from abc import ABCMeta, abstractmethod
import multiprocessing
from queue import Queue


class IGeneratorController (metaclass=ABCMeta):
    """
    生成処理プロセスのコントローラインターフェース

    Webプロセスからのリクエストを受け取り、必要に応じてタスクキューに格納する。
    """

    @abstractmethod
    def listen(self, recv_queue:multiprocessing.Queue, task_queue:Queue):
        """
        リクエストの受付を開始する。
        """
        pass

class IGenerator (metaclass=ABCMeta):
    """
    生成処理のインターフェース
    """

    @abstractmethod
    def process(self, task_queue:Queue, result_queue:Queue):
        """
        登録されたタスクを処理する。
        """
        pass

class IGeneratorPresenter (metaclass=ABCMeta):
    """
    生成処理のプレゼンターインターフェース

    生成処理のメッセージを受け取り、Webプロセスに送信する。
    """

    @abstractmethod
    def send(self, result_queue:Queue, send_queue:multiprocessing.Queue):
        """
        生成処理のメッセージを送信する。
        """
        pass