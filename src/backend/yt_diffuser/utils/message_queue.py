"""
メッセージキューのユーティリティ

主に形式の統一のためのもの。
"""
from enum import Enum
import logging; logger = logging.getLogger(__name__)

from multiprocessing import Queue

class EventType (Enum):
    """
    イベントの種類
    """
    GENERATE_STATUS = 'generator'
    FILESYSTEM = 'filesystem'

class GenerateStatus (Enum):
    """
    生成ステータス
    """
    EXIt = 'exit'
    LOADING = 'loading'
    READY = 'ready'
    GENERATING = 'generating'


def send_generate_status (queue: Queue, status: GenerateStatus, **kwargs):
    """
    生成ステータスイベントを送信する。

    params:
        queue: 送信キュー
        status: ステータス
        kwargs: その他のパラメータ
    """
    if kwargs is None:
        kwargs = {}

    data = kwargs
    data['status'] = status.value
    queue.put((EventType.GENERATE_STATUS.value, data), timeout=1)


def send_ready (queue: Queue, event: str, target: str):
    """
    準備完了イベントを送信する。

    この関数は特定のイベント名は持たない。

    params:
        queue: 送信キュー
        event: イベント名
        target: ターゲット名
    """
    queue.put((event, {
        'target': target,
        'status': 'ready'
    }))


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
        'status': 'progress',
        'total': total,
        'progress': progress,
        'percentage': percentage,
        'elapsed': elapsed,
        'remaining': remaining
    }))


def send_filesystem (queue: Queue, type: str, target: str):
    """
    ファイルシステムイベントを送信する。

    params:
        queue: 送信キュー
        type: 変更の種類
            - created: 作成
            - modified: 更新
            - deleted: 削除
        target: 対象ファイルパス
    """
    queue.put((EventType.FILESYSTEM.value, {
        'type': type,
        'target': target
    }))