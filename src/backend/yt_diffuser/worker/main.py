""" データ処理プロセスのメイン処理
"""
from logging import getLogger; logger = getLogger(__name__)
import os

from multiprocessing.queues import Queue

from yt_diffuser.config import AppConfig
from yt_diffuser.worker.web_sender import set_send_queue
from yt_diffuser.worker.web_listener import start_listener
from yt_diffuser.worker.worker import start_worker


def worker_procedure(config:AppConfig, send_queue:Queue, recv_queue:Queue):
    if os.environ.get('DEBUG') == '1':
        import logging; logging.basicConfig(level=logging.DEBUG)
    
    logger.debug('Worker process started...')

    set_send_queue(send_queue)

    send_queue.put(('status', 'empty'))

    start_listener(recv_queue)
    start_worker(config)
