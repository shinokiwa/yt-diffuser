""" Flaskのアプリ定義
"""
import atexit
from logging import getLogger; logger = getLogger(__name__)

from flask import Flask

from yt_diffuser.config import AppConfig
from yt_diffuser.web.route import init_routes
from yt_diffuser.store.db.setup import setup_database
from yt_diffuser.utils.event import start_message_listener

def create_app (config:AppConfig):
    """ Flaskのアプリを作成する
    """
    app = Flask(__name__)
    app.config['APP_CONFIG'] = config

    init_routes(app)

    start_message_listener()

    setup_database(
        db_file=config.DB_FILE,
        db_update_file=config.DB_UPDATE_FILE,
        db_version=config.DB_VERSION
    )

    return app
