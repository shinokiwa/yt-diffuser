""" ヘルスチェックAPIのパッケージ
"""
from flask import Blueprint

health_bp = Blueprint('api_health', __name__)

@health_bp.route('/api/health', methods=['GET'])
def health ():
    """ ヘルスチェック
    """
    return 'ok'