""" worker_sender.py
"""

from multiprocessing.queues import Queue

_send_queue:Queue = None

def set_send_queue (queue:Queue):
    """ ワーカープロセスに指示を出すキューを設定する
    """
    global _send_queue
    _send_queue = queue

def get_send_queue () -> Queue:
    """ ワーカープロセスに指示を出すキューを取得する
    """
    return _send_queue