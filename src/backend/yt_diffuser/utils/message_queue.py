"""
メッセージキューのユーティリティ

主に形式の統一のためのもの。
"""
import logging; logger = logging.getLogger(__name__)

from multiprocessing import Queue

EVENT_TYPE_MESSAGE = 'message'


def send_message (queue: Queue, label: str, **kwargs):
    """
    メッセージイベントを送信する。

    params:
        queue: 送信キュー
        label: メッセージラベル
        kwargs: その他のパラメータ
    """
    data = kwargs
    data['label'] = label
    queue.put((EVENT_TYPE_MESSAGE, data), timeout=1)


def send_progress (queue: Queue, event: str, target: str, total: int, progress: int, percentage: float, elapsed: float, remaining: float):
    """
    進捗イベントを送信する。

    この関数は特定のイベント名は持たない。

    params:
        queue: 送信キュー
        event: イベント名
        target: ターゲット名
        total: 全体の数
        progress: 進捗数
        percentage: パーセンテージ
        elapsed: 経過時間
        remaining: 残り時間
    """
    queue.put((event, {
        'target': target,
        'total': total,
        'progress': progress,
        'percentage': percentage,
        'elapsed': elapsed,
        'remaining': remaining
    }))