""" tqdmをオーバーライドするクラス
"""
from multiprocessing.queues import Queue

from tqdm import tqdm

class WorkerProgress(tqdm):
    """ tqdmをオーバーライドし、進捗を標準出力ではなく送信キューに入れる。
    ワーカー進捗用。
    """
    def __init__(self, iterable=None, desc=None, total=None, leave=True, file=None,
                 ncols=None, mininterval=0.1, maxinterval=10.0, miniters=None,
                 ascii=None, disable=False, unit='it', unit_scale=False,
                 dynamic_ncols=False, smoothing=0.3, bar_format=None, initial=0,
                 position=None, postfix=None, unit_divisor=1000, write_bytes=False,
                 lock_args=None, nrows=None, colour=None, delay=0.0, gui=False,
                 queue: Queue = None, status: str = None, target: str = None,
                 **kwargs):

        self.queue: Queue = queue
        self.status: str = status
        self.target: str = target

        super().__init__(
            iterable=iterable, desc=desc, total=total, leave=leave, file=file,
            ncols=ncols, mininterval=mininterval, maxinterval=maxinterval, miniters=miniters,
            ascii=ascii, disable=disable, unit=unit, unit_scale=unit_scale,
            dynamic_ncols=dynamic_ncols, smoothing=smoothing, bar_format=bar_format, initial=initial,
            position=position, postfix=postfix, unit_divisor=unit_divisor, write_bytes=write_bytes,
            lock_args=lock_args, nrows=nrows, colour=colour, delay=delay, gui=gui,
            **kwargs
        )

    def display(self, msg: str | None = None, pos: int | None = None) -> None:
        """ 進捗を送信キューに入れる。

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
            self.queue.put_nowait((self.status, {
                'target': self.target,
                'total': total,
                'progress': self.n,
                'percentage': percentage,
                'elapsed': elapsed,
                'remaining': remaining
            }))

        return True
