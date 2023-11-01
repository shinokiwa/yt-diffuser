""" APIのエラーハンドラー
"""

from flask import Blueprint, jsonify
from werkzeug.exceptions import HTTPException

def handle_http_exception(e) -> tuple:
    """ 例外ハンドラー
    """
    response = {
        "error": e.description
    }
    return jsonify(response), e.code

def register_errorhandler (bp: Blueprint) -> None:
    """ エラーハンドラーを登録する
    """
    bp.register_error_handler(HTTPException, handle_http_exception)