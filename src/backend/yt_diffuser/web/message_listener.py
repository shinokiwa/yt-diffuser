""" ワーカープロセスからのメッセージを受け取るモジュール
"""
from logging import getLogger; logger = getLogger(__name__)
import multiprocessing
import threading
import queue

from queue import Empty # このモジュールでは使わないが、インポート先で確定的に使うのでここでインポートしておく

_listeners = {}
_latest_messages = {}
_NO_CACHE_EVENT = [
    'message'
] # 最終メッセージをキャッシュしないイベント

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
    latest_message = _latest_messages.get(event_name, "")
    q.put_nowait(latest_message)

    _listeners[event_name].append(q)

    logger.debug(f"Add listener for {event_name}.")

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

    logger.debug(f"Remove listener for {event_name}.")

_context = multiprocessing.get_context('spawn')

def get_context() -> multiprocessing.context.SpawnContext:
    """
    プロセスコンテキストを取得する。

    Returns:
        multiprocessing.context.SpawnContext: プロセスコンテキスト
    """
    return _context

_message_queue = _context.Queue()

def get_message_queue() -> multiprocessing.Queue:
    """
    メッセージキューを取得する。

    - メッセージキューは他プロセスがWebプロセスに対してメッセージを送信するために使用する。
    - 受け取ったメッセージはメッセージリスナーによってイベントリスナーに配信される。
    
    Returns:
        multiprocessing.Queue: メッセージキューのインスタンス。
    """
    return _message_queue


def message_listener() -> None:
    """
    メッセージキューからメッセージを受け取り、イベントリスナーに配信する。

    - イベントが "exit" の場合、リスナーを終了する。
    - 最新のメッセージは _latest_messages に格納され、新規リスナーには最新のメッセージが配信される。
    - _NO_CACHE_EVENT に指定されたイベントは最新メッセージをキャッシュしない。

    Returns:
        None
    """
    logger.debug("Start message listener.")
    queue = get_message_queue()
    while True:
        (event, data) = queue.get()

        if event == "exit":
            break

        if event not in _NO_CACHE_EVENT:
            _latest_messages[event] = data

        for listener in _listeners.get(event, []):
            listener.put_nowait(data)
    logger.debug("Exit message listener.")


def start_message_listener () -> None:
    """
    メッセージリスナーを起動する。

    - メッセージリスナーは別スレッドで起動する。
    - メッセージリスナーはプロセス終了時に自動的に終了する。
    """
    logger.debug("Call message listener.")

    threading.Thread(
        target=message_listener,
        daemon=True
    ).start()

def stop_message_listener () -> None:
    """
    メッセージリスナーを終了する。

    - メッセージリスナーはプロセス終了時に自動的に終了するため、通常は呼び出す必要はない。
    - テストの連続実行時はプロセスが終了しないため、明示的に終了する必要がある。
    """
    logger.debug("Call stop message listener.")

    get_message_queue().put_nowait(("exit", None))