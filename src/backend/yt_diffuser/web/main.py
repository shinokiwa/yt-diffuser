""" Web APIプロセスのメイン処理
"""
from logging import getLogger; logger = getLogger(__name__)

import os
import asyncio

from waitress import serve

from multiprocessing.connection import Connection

from yt_diffuser.web.app import create_app
from yt_diffuser.web.connection import set_shared_conn
from yt_diffuser.web.worker_listener import start_listener

def web_procedure(shared_conn:Connection) -> None:
    """ Webメイン処理

    Flaskを使ったWeb APIを起動する
    """

    if os.environ.get('DEBUG') == '1':
        import logging; logging.basicConfig(level=logging.DEBUG)

    logger.debug('Start Web API')

    set_shared_conn(shared_conn)

    app = create_app()
    asyncio.run(start_listener())

    if os.environ.get('DEBUG') == '1':
        app.debug = True

    serve(app, host='0.0.0.0', port=8000)
