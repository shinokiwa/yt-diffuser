from threading import Thread

from .interface import IThreadStore, ThreadKeys

class ThreadStore(IThreadStore):
    """
    スレッドストア
    """

    threads = {}

    def __init__(self):
        """
        コンストラクタ
        """
        pass

    def create_thread(self, key:ThreadKeys, target, args=(), kwargs={}) -> Thread:
        """
        スレッドデータを作成してストックする。
        同一キーが存在する場合は上書きする。

        Args:
            key (ThreadKey): スレッド名
            target (function): スレッドの実行関数
            args (tuple): 引数
            kwargs (dict): キーワード引数
        """
        if self.is_alive(key):
            raise Exception("Thread already exists.")

        thread = Thread(target=target, args=args, kwargs=kwargs)
        self.__class__.threads[key] = thread
        return thread

    def get_thread(self, key:ThreadKeys):
        """
        スレッドデータを取得する。
        存在しない場合はNoneを返す。

        Args:
            key (ThreadKeys): スレッド名

        Returns:
            ThreadData: スレッドデータ
        """
        return self.__class__.threads.get(key)

    def is_alive(self, key:ThreadKeys) -> bool:
        """
        スレッドが生存しているかどうかを返す。

        Args:
            key (ThreadKeys): スレッド名

        Returns:
            bool: 生存しているかどうか
        """
        thread_data = self.get_thread(key)
        if thread_data is None:
            return False
        return thread_data['thread'].is_alive()
