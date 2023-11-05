""" ワーカープロセスからのメッセージを受け取るモジュール
"""
from logging import getLogger; logger = getLogger(__name__)
import threading
import queue
from multiprocessing.queues import Queue

from yt_diffuser.util.loop import infinite_loop

from queue import Empty

_listeners = {}
_latest_messages = {}

def get_listener(event_name:str) -> queue.Queue:
    """ 指定したイベントのリスナーキューを取得する
    リスナーキューは初期状態で最新のメッセージが入っている
    """
    if event_name not in _listeners:
        _listeners[event_name] = []

    q = queue.Queue()
    latest_message = _latest_messages.get(event_name, None)
    if latest_message is not None:
        q.put_nowait(latest_message)

    _listeners[event_name].append(q)

    logger.debug(f"Add listener for {event_name}.")

    return q


def remove_listener(event_name:str, listener:queue.Queue):
    """ リスナーキューを削除する
    """
    if event_name not in _listeners:
        return

    if listener in _listeners[event_name]:
        _listeners[event_name].remove(listener)

    logger.debug(f"Remove listener for {event_name}.")

def msg_callback(msg):
    """ メッセージ受信コールバック
    """
    (event, data) = msg
    _latest_messages[event] = data

    for listener in _listeners.get(event, []):
        listener.put_nowait(data)


def start_listener (queue:Queue):
    """ リスナーを起動する
    """
    logger.debug("Start worker listener.")

    threading.Thread(target=infinite_loop, args=(queue, msg_callback), daemon=True).start()
