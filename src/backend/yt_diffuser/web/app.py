""" Flaskのアプリ定義
"""
from logging import getLogger; logger = getLogger(__name__)
from pathlib import PurePath

from flask import Flask
from u_dam.sqlite3 import setup_database, connect_database

from yt_diffuser.config import AppConfig
from yt_diffuser.web.route import init_routes
from yt_diffuser.utils.event import start_message_listener

def create_app (config:AppConfig):
    """ Flaskのアプリを作成する
    """
    app = Flask(__name__)
    app.config['APP_CONFIG'] = config

    init_routes(app)

    start_message_listener()
    if isinstance(config.DB_FILE, PurePath):
        config.DB_FILE.parent.mkdir(parents=True, exist_ok=True)

    setup_database(
        connection_method=connect_database,
        database_path=str(config.DB_FILE),
        package_name="yt_diffuser.database",
    )

    return app
