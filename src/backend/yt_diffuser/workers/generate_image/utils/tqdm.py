""" tqdmをオーバーライドするクラス
"""
from multiprocessing.queues import Queue

from tqdm import tqdm

from yt_diffuser.utils.event import GenerateProgressEvent

class GenerateProgressTqdm(tqdm):
    """
    tqdmをオーバーライドし、進捗を標準出力ではなく送信キューに入れる。

    生成処理の進捗用。
    """
    def __init__(self, iterable=None,
                 total=None,
                 mininterval=0.1,
                 maxinterval=10.0,
                 miniters=None,
                 initial=0,
                 queue: Queue = None,
                 generate_total: int = None,
                 generate_count: int = None,
                 average: float = 0,
                 **kwargs):

        self.queue: Queue = queue
        self.generate_total: int = generate_total
        self.generate_count: int = generate_count
        self.average: float = average

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
            GenerateProgressEvent.send_process(
                process_queue=self.queue,
                generate_total=self.generate_total,
                generate_count=self.generate_count,

                steps_total=total,
                steps_count=self.n,

                percentage=percentage,
                elapsed=elapsed,
                remaining=remaining,
                average=self.average
            )

        return True
