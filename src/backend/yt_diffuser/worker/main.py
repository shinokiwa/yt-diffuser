""" データ処理プロセスのメイン処理
"""
from logging import getLogger; logger = getLogger(__name__)
import os

import gevent
from multiprocessing.connection import Connection

from yt_diffuser.worker.connection import set_shared_conn
from yt_diffuser.worker.worker import dispatch

def worker_procedure(shared_conn:Connection, parent_conn:Connection):
    if os.environ.get('DEBUG') == '1':
        import logging; logging.basicConfig(level=logging.DEBUG)
    
    from gevent import monkey; monkey.patch_all()

    logger.debug('Worker process started...')

    set_shared_conn(shared_conn)

    while True:
        if shared_conn.closed:
            gevent.sleep(1)
            continue

        try:
            if shared_conn.poll(timeout=1):
                msg = shared_conn.recv()
                dispatch(msg[0], msg[1])
        except EOFError:
            pass
