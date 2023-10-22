"""model関連のAPIモジュール
"""
from flask import Blueprint, request, abort, current_app

model_bp = Blueprint('api_model', __name__)

@model_bp.route('/model', methods=['GET'])
def get_model ():
    """保存済みのモデル一覧を取得する
    """
    data = {}
    data['models'] = []

    return data