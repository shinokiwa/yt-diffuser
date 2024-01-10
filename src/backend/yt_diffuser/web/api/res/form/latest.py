"""
最後にフォームに入力した値を保存、取得するAPI
"""
from flask import Blueprint, request, current_app
from pydantic import BaseModel, ValidationError

from yt_diffuser.config import AppConfig
from yt_diffuser.store.db import connect_database
from yt_diffuser.store.db.op.form_data import (
    save,
    get_all,
    delete
)

bp = Blueprint('api_res_form_latest', __name__)

class FormData(BaseModel):
    """
    フォームのデータを保存するためのモデル。
    初期値は全てNoneで、Noneは入力されていないことを表す。
    空を入力されたフォームは空文字列として保存される。
    """
    model_name: str = None
    revision: str = None

    seed: int = None
    prompt: str = None
    negative_prompt: str = None
    inference_steps: int = None


@bp.route('/api/res/form/latest', methods=['GET'])
def get_form_latest ():
    """
    最後にフォームに入力した値を取得する。
    ついでに不要なレコードを削除する。
    """
    config = current_app.config['APP_CONFIG']
    with connect_database(config.DB_FILE) as conn:
        data = get_all(conn)
        
        kv = {}
        for d in data:
            if d['name'] in FormData.__fields__:
                kv[d['name']] = d['value']
            else:
                delete(conn, d['name'])

    return kv

@bp.route('/api/res/form/latest', methods=['POST'])
def post_form_latest ():
    """
    最後にフォームに入力した値を保存する。
    """
    config = current_app.config['APP_CONFIG']
    try:
        form = FormData(**request.json)
    except ValidationError as e:
        return {'error': e.errors()}, 400

    with connect_database(config.DB_FILE) as conn:
        # Noneは保存しない
        data = {}
        for key, value in form.dict().items():
            if value is not None:
                data[key] = value
        
        if len(data) > 0:
            save(conn, **data)
            return {'result': 'ok'}
        else:
            return {'result': 'no data'}, 400
