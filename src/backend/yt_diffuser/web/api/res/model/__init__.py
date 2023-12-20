"""model関連のAPIモジュール
"""
from flask import Blueprint, current_app

from yt_diffuser.config import AppConfig
from yt_diffuser.store import connect_database, ModelStore, MODEL_CLASS_NAME
from yt_diffuser.store.store_utils import model_factory
from yt_diffuser.store.db.op.models import get_all, delete

bp = Blueprint('api_res_model', __name__)

@bp.route('/api/res/model', methods=['GET'])
def get_model ():
    """
    保存済みのモデル一覧を取得する。


    """
    config:AppConfig = current_app.config['APP_CONFIG']
    with connect_database(config.DB_FILE) as conn:

        _models = get_all(conn)

        models = []
        for model in _models:
            if model['class_name'] not in MODEL_CLASS_NAME.values():
                delete(conn, model['model_name'], model['revision'])
                continue
            
            store = model_factory(
                config=config,
                model_name=model['model_name'],
                revision=model['revision'],
                class_name=model['class_name']
            )

            if store.exists():
                models.append({
                    'model_name': model['model_name'],
                    'revision': model['revision'],
                    'class_name': model['class_name']
                })

        data = {'models': models}

        conn.commit()

    return data
