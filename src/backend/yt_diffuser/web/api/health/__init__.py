""" ヘルスチェックAPIのパッケージ
"""
from flask import Blueprint

bp = Blueprint('api_health', __name__)

@bp.route('/api/health', methods=['GET'])
def health () -> str:
    """
    ヘルスチェック

    - ヘルスチェックとして、'ok'を返す。

    Returns:
        str: 'ok'
    """
    return 'ok'