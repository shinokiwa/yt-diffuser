"""model関連のAPIモジュール
"""
from flask import Blueprint

model_bp = Blueprint('api_res_model', __name__)

@model_bp.route('/api/res/model', methods=['GET'])
def get_model ():
    """保存済みのモデル一覧を取得する
    """
    data = {}
    data['models'] = []

    return data
