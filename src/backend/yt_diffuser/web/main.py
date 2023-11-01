""" Web APIプロセスのメイン処理
"""
from logging import getLogger; logger = getLogger(__name__)

import os

from gevent.pywsgi import WSGIServer

from multiprocessing.connection import Connection

from yt_diffuser.web.app import create_app
from yt_diffuser.web.connection import set_shared_conn
from yt_diffuser.web.worker_listener import start_greenlets

def web_procedure(shared_conn:Connection, parent_conn:Connection) -> None:
    """ Webメイン処理

    Flaskを使ったWeb APIを起動する
    """

    from gevent import monkey; monkey.patch_all()
    if os.environ.get('DEBUG') == '1':
        import logging; logging.basicConfig(level=logging.DEBUG)

    logger.debug('Start Web API')

    set_shared_conn(shared_conn)

    app = create_app()
    start_greenlets()

    if os.environ.get('DEBUG') == '1':
        app.debug = True

    http_server = WSGIServer(('0.0.0.0', 8000), app)
    http_server.serve_forever()
