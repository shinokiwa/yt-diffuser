""" ルーティングを設定する
"""
from importlib import import_module

from flask import Flask, Blueprint

def init_routes (app:Flask):
    """ ルーティングを設定する
    """
    # /api/配下のみエラーハンドラーを設定するため、一時的にブループリントを作成する
    api = Blueprint('api', __name__)

    from yt_diffuser.web.api.errorhandler import register_errorhandler
    register_errorhandler(api)

    api.register_blueprint(import_module('yt_diffuser.web.api.health').bp)
    #from yt_diffuser.web.api.health import health_bp
    #api.register_blueprint(health_bp)

    api.register_blueprint(import_module('yt_diffuser.web.api.download').bp)
   
    #from yt_diffuser.web.api.res.model import model_bp
    #api.register_blueprint(model_bp)

    api.register_blueprint(import_module('yt_diffuser.web.api.sse.sse').bp)

    #from yt_diffuser.web.api.worker import worker_bp
    #api.register_blueprint(worker_bp)

    app.register_blueprint(api)