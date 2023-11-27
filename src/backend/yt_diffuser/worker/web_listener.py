""" Webプロセスからのメッセージを受け取るモジュール
"""
from logging import getLogger; logger = getLogger(__name__)
import threading
from multiprocessing.queues import Queue

from yt_diffuser.util.loop import infinite_loop
from yt_diffuser.worker.worker import get_worker_loop, get_worker_queue

def msg_callback(msg):
    """ メッセージ受信コールバック
    """

    logger.debug(f"Web message received: {msg}")
    worker_loop = get_worker_loop()

    if worker_loop is not None:

        worker_queue = get_worker_queue()
        worker_loop.call_soon_threadsafe(worker_queue.put_nowait, msg)
    else:
        logger.warning("Worker loop is not started.")


def start_listener (queue:Queue):
    """ リスナーを起動する
    """
    logger.debug("Start web listener.")

    threading.Thread(target=infinite_loop, args=(queue, msg_callback), daemon=True).start()