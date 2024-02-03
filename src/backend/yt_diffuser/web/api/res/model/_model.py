"""model関連のAPIモジュール
"""
from flask import Blueprint, current_app

from yt_diffuser.config import AppConfig
from yt_diffuser.database import connect_database
from yt_diffuser.store.store_utils import get_model_list

bp = Blueprint('api_res_model', __name__)

@bp.route('/api/res/model', methods=['GET'])
def get_model ():
    """
    保存済みのモデル一覧を取得する。


    """
    config:AppConfig = current_app.config['APP_CONFIG']
    with connect_database(config.DB_FILE) as conn:

        models = get_model_list(config, conn)
        data = {'models': models}
    
    return data
