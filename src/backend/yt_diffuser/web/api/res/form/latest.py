"""
最後にフォームに入力した値を保存、取得するAPI
"""
from flask import Blueprint, request, current_app
from pydantic import BaseModel, validator, ValidationError

from yt_diffuser.config import AppConfig
from yt_diffuser.database import connect_database
from yt_diffuser.database.tables.form_data import (
    save,
    get_all,
    delete_not_in
)

bp = Blueprint('api_res_form_latest', __name__)

class FormData(BaseModel):
    """
    フォームのデータを保存するためのモデル。
    初期値は全てNoneで、Noneは入力されていないことを表す。
    空を入力されたフォームは空文字列として保存される。
    """
    base_model_name: str = None
    base_model_revision: str = None
    compile: bool = None

    lora_model_name: str = None
    lora_model_revision: str = None
    lora_model_weight: str = None

    controlnet_model_name: str = None
    controlnet_model_revision: str = None
    controlnet_model_weight: str = None

    seed: str = None
    generate_type: str = None

    width: int = None
    height: int = None

    prompt: str = None
    negative_prompt: str = None
    scheduler: str = None
    inference_steps: int = None
    guidance_scale: float = None

    strength: float = None

    memo: str = None

    @validator('compile', pre=True)
    def compile_to_bool(cls, v):
        """
        compileはboolまたは'1'/'0'を受け付けて、boolに変換する。
        """
        if isinstance(v, bool):
            return v
        elif v == '1':
            return True
        elif v == '0':
            return False
        else:
            raise ValueError('invalid value')

@bp.route('/api/res/form/latest', methods=['GET'])
def get_form_latest ():
    """
    最後にフォームに入力した値を取得する。
    ついでに不要なレコードを削除する。
    """
    config = current_app.config['APP_CONFIG']
    with connect_database(config.DB_FILE) as conn:
        delete_not_in(conn, list(FormData.__fields__.keys()))

        data = get_all(conn)

        # FormDataのバリデーションを使って型変換する。
        # 保存時にバリデーションを通しているので、ここでエラーになることはない想定。
        try:
            form = FormData(**data)
            return form.dict()

        except ValidationError as e:
            return {'error': e.errors()}, 500
        


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
