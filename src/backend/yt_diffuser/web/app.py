""" Flaskのアプリ定義
"""
from flask import Flask

from yt_diffuser.web.route import init_routes

def create_app ():
    """ Flaskのアプリを作成する
    """
    app = Flask(__name__)
    init_routes(app)

    return app