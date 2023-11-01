""" ルーティングを設定する
"""
from flask import Flask, Blueprint

def init_routes (app:Flask):
    """ ルーティングを設定する
    """
    api = Blueprint('api', __name__)
    from yt_diffuser.web.api.errorhandler import register_errorhandler
    register_errorhandler(api)

    from yt_diffuser.web.api.res.model import model_bp
    api.register_blueprint(model_bp)

    from yt_diffuser.web.api.sse import sse_bp
    api.register_blueprint(sse_bp)

    from yt_diffuser.web.api.worker import worker_bp
    api.register_blueprint(worker_bp)

    app.register_blueprint(api)