""" APIモジュール
"""
from flask import Flask, Blueprint, jsonify
from werkzeug.exceptions import HTTPException

api = Blueprint('api', __name__)

@api.app_errorhandler(HTTPException)
def handle_http_exception(e):
    response = {
        "error": e.description
    }
    return jsonify(response), e.code

from .model import model_bp; api.register_blueprint(model_bp)
from .sse import sse_bp; api.register_blueprint(sse_bp)

def regist_api (app: Flask) -> None:
    """ APIのBlueprintを登録する
    """
    app.register_blueprint(api, url_prefix='/api')


