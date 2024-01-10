"""model関連のAPIモジュール
"""
from flask import Blueprint, current_app

from yt_diffuser.config import AppConfig
from yt_diffuser.store import connect_database
from yt_diffuser.store.store_utils import scan_model_dir

bp = Blueprint('api_res_model', __name__)

@bp.route('/api/res/model', methods=['GET'])
def get_model ():
    """
    保存済みのモデル一覧を取得する。


    """
    config:AppConfig = current_app.config['APP_CONFIG']
    with connect_database(config.DB_FILE) as conn:

        _models = scan_model_dir(config, conn)

        models = []
        for model in _models:
            data = model.to_dict()
            models.append(data)

        data = {'models': models}

        conn.commit()

    return data
