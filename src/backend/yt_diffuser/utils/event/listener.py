"""
イベントリスナーの処理を行うモジュール
"""
from logging import getLogger; logger = getLogger(__name__)

import queue

_listeners = {}
_latest_messages = {}

def get_event_listener(event_name:str) -> queue.Queue:
    """
    指定したイベントのリスナーキューを作成し、取得する。

    - リスナーキューは最初に最新のキャッシュメッセージが格納される。
    - 未登録のイベント名の場合はイベントを作成する。
    - ハートビートも兼ねて、最新のメッセージがない場合は空文字列が格納される。
    - 使用後は remove_event_listener で削除すること。

    Args:
        event_name (str): イベント名

    Returns:
        queue.Queue: リスナーキューオブジェクト

    """
    if event_name not in _listeners:
        _listeners[event_name] = []

    q = queue.Queue()
    latest_message = _latest_messages.get(event_name)
    if latest_message != None:
        q.put(latest_message)

    _listeners[event_name].append(q)

    logger.debug(f"Add listener for {event_name}. id={id(q)}")

    return q


def remove_event_listener(event_name: str, listener: queue.Queue):
    """
    リスナーキューを削除する。

    - 未登録のイベント名、リスナーキューの場合は何もしない。

    Args:
        event_name (str): イベント名
        listener (queue.Queue): 削除するリスナーキュー

    Returns:
        None
    """
    if event_name not in _listeners:
        return

    if listener in _listeners[event_name]:
        _listeners[event_name].remove(listener)

    if len(_listeners[event_name]) == 0:
        del _listeners[event_name]

    logger.debug(f"Remove listener for {event_name}. id={id(listener)}")


def send_event(event_name: str, cache:bool = True, data: dict | None = None) -> None:
    """
    イベントリスナーにイベントを配信する。

    args:
        event_name (str): イベント名
        cache (bool): キャッシュするかどうか
        data (dict): イベントデータ
    """
    if cache:
        _latest_messages[event_name] = data

    for listener in _listeners.get(event_name, []):
        logger.debug(f"Put message to listener. id={id(listener)}")
        _data = data.copy() if type(data) == dict else data
        listener.put(_data)