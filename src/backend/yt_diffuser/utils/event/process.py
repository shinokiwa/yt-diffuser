"""
別プロセスからのイベントを受信するためのモジュール
"""
from logging import getLogger; logger = getLogger(__name__)
import atexit
import multiprocessing
from multiprocessing.context import SpawnContext
import threading

from yt_diffuser.utils.event.listener import send_event

_context = multiprocessing.get_context('spawn')

def get_context() -> SpawnContext:
    """
    プロセスコンテキストを取得する。

    Returns:
        SpawnContext: プロセスコンテキスト
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
        (event_name, cache, data) = queue.get()

        if event_name == "exit":
            break

        logger.debug(f"Received message : {event_name}")
        send_event(event_name, cache, data)

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
    atexit.register(stop_message_listener)

def stop_message_listener () -> None:
    """
    メッセージリスナーを終了する。

    - メッセージリスナーはプロセス終了時に自動的に終了するため、通常は呼び出す必要はない。
    - テストの連続実行時はプロセスが終了しないため、明示的に終了する必要がある。
    """
    logger.debug("Call stop message listener.")

    get_message_queue().put_nowait(("exit", False, None))

