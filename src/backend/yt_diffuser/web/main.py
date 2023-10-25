""" Web APIプロセスのメイン処理
"""
from logging import getLogger; logger = getLogger(__name__)
import os
from gevent.pywsgi import WSGIServer
from multiprocessing.connection import Connection

from . import app

def web_procedure(shared_conn:Connection, parent_conn:Connection) -> None:
    """ Webメイン処理

    Flaskを使ったWeb APIを起動する
    """
    logger.debug('Start Web API')

    app.shared_conn = shared_conn

    http_server = WSGIServer(('', 8000), app.app)
    http_server.serve_forever()
