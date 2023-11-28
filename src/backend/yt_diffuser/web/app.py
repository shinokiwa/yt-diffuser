""" Flaskのアプリ定義
"""
from flask import Flask

from yt_diffuser.config import AppConfig
from yt_diffuser.web.route import init_routes

def create_app (config:AppConfig):
    """ Flaskのアプリを作成する
    """
    app = Flask(__name__)
    app.config.from_object(config)

    init_routes(app)

    return app