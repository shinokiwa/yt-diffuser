""" tqdmをオーバーライドするクラス
"""
from tqdm import tqdm
from datetime import datetime, timedelta

from yt_diffuser.worker.web_sender import get_send_queue

class WorkerProgress(tqdm):
    """ tqdmをオーバーライドし、進捗を標準出力ではなく送信キューに入れる。
    ワーカー進捗用。
    """

    cancelable: bool = True

    def display(self, msg: str | None = None, pos: int | None = None) -> None:
        """ 進捗を送信キューに入れる。

        params:
            msg: 進捗メッセージ。使用しない。
            pos: 進捗バーの位置。使用しない。
        """
        # 進捗のパーセンテージを計算
        percentage = 0
        if self.total != 0:
            percentage = self.n / self.total * 100

        # 経過時間を取得
        elapsed = self.format_dict['elapsed']

        # 予測残り時間を計算
        if self.total == 0 or elapsed == 0 or (self.n - self.initial) == 0:
            remaining = -1
        else:
            rate = (self.n - self.initial) / elapsed
            remaining = (self.total - self.n) / rate

        # 出力
        q = get_send_queue()
        q.put(('progress', {
            'cancelable': self.cancelable,
            'total': self.total,
            'progress': self.n,
            'percentage': percentage,
            'elapsed': elapsed,
            'remaining': remaining
        }))

        return True

class DownloadProgress(WorkerProgress):
    """ tqdmをオーバーライドし、進捗を標準出力ではなく送信キューに入れる。
    ダウンロード進捗用。
    単にキャンセルNGなだけ。
    """

    cancelable: bool = False
