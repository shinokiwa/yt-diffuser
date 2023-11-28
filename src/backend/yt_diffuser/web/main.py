""" Web APIプロセスのメイン処理
"""
from logging import getLogger; logger = getLogger(__name__)

import os
from multiprocessing.queues import Queue

from waitress import serve

from yt_diffuser.config import AppConfig
from yt_diffuser.web.app import create_app
from yt_diffuser.web.worker_listener import start_listener
from yt_diffuser.web.worker_sender import set_send_queue

def web_procedure(config:AppConfig, send_queue:Queue, recv_queue:Queue) -> None:
    """ Webメイン処理

    Flaskを使ったWeb APIを起動する
    """

    if os.environ.get('DEBUG') == '1':
        import logging; logging.basicConfig(level=logging.DEBUG)

    logger.debug('Start Web API')


    app = create_app(config)
    start_listener(recv_queue)
    set_send_queue(send_queue)

    if os.environ.get('DEBUG') == '1':
        app.debug = True

    serve(app, host='0.0.0.0', port=8000)
