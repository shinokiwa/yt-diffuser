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
    api.register_blueprint(import_module('yt_diffuser.web.api.download').bp)

    api.register_blueprint(import_module('yt_diffuser.web.api.generate.process').bp)
    api.register_blueprint(import_module('yt_diffuser.web.api.generate.image').bp)
    api.register_blueprint(import_module('yt_diffuser.web.api.generate.preview').bp)
    api.register_blueprint(import_module('yt_diffuser.web.api.generate.status').bp)
    api.register_blueprint(import_module('yt_diffuser.web.api.generate.progress').bp)
   
    api.register_blueprint(import_module('yt_diffuser.web.api.res.form.latest').bp)
    api.register_blueprint(import_module('yt_diffuser.web.api.res.form.prompt').bp)
    api.register_blueprint(import_module('yt_diffuser.web.api.res.model').bp)
    api.register_blueprint(import_module('yt_diffuser.web.api.res.output').bp)

    api.register_blueprint(import_module('yt_diffuser.web.api.res.input.image').bp)

    app.register_blueprint(api)