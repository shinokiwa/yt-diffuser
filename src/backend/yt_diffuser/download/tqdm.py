""" tqdmをオーバーライドするクラス
"""
from multiprocessing.queues import Queue

from tqdm import tqdm

from yt_diffuser.utils.event import DownloadStatusEvent

class DownloadProgress(tqdm):
    """
    tqdmをオーバーライドし、進捗を標準出力ではなく送信キューに入れる。

    ワーカー進捗用。
    """
    def __init__(self, iterable=None,
                 total=None,
                 mininterval=0.1,
                 maxinterval=10.0,
                 miniters=None,
                 initial=0,
                 queue: Queue = None,
                 model_name: str = None,
                 revision: str = None,
                 **kwargs):

        self.queue: Queue = queue
        self.model_name: str = model_name
        self.revision: str = revision

        super().__init__(
            iterable=iterable,
            total=total,
            mininterval=mininterval,
            maxinterval=maxinterval,
            miniters=miniters,
            initial=initial,
            **kwargs
        )

    def display(self, msg: str | None = None, pos: int | None = None) -> None:
        """
        進捗を送信キューに入れる。

        キューが指定されていない場合は何もしない。

        params:
            msg: 進捗メッセージ。使用しない。
            pos: 進捗バーの位置。使用しない。
        """
        # 進捗のパーセンテージを計算
        percentage = 0
        total = self.total if self.total is not None else 0
        
        if total != 0:
            percentage = self.n / total * 100

        # 経過時間を取得
        elapsed = self.format_dict['elapsed']

        # 予測残り時間を計算
        if total == 0 or elapsed == 0 or (self.n - self.initial) == 0:
            remaining = -1
        else:
            rate = (self.n - self.initial) / elapsed
            remaining = (total - self.n) / rate
        
        # 出力
        if self.queue:
            DownloadStatusEvent.send_process(
                process_queue=self.queue,
                status=DownloadStatusEvent.Status.DOWNLOADING,
                model_name=self.model_name,
                revision=self.revision,
                total=total,
                progress=self.n,
                percentage=percentage,
                elapsed=elapsed,
                remaining=remaining,
            )

        return True
