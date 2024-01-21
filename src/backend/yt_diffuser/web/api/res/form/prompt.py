"""
プロンプト保存のAPI
"""
from flask import Blueprint, request, current_app
from pydantic import BaseModel, ValidationError

from yt_diffuser.config import AppConfig
from yt_diffuser.database import connect_database
from yt_diffuser.database.tables.prompt_archive import (
    insert,
    update,
    get_by_type,
    delete,
    Types
)

bp = Blueprint('api_res_form_prompt', __name__)

class PromptData(BaseModel):
    """
    プロンプトのデータを保存するためのモデル。
    """
    prompt: str

@bp.route('/api/res/form/prompt', methods=['GET'])
def get_form_prompt ():
    """
    プロンプトを取得する。
    プロンプトは最終更新日時の降順で取得する。
    （更新日時が同じ場合はIDの降順）
    """
    config = current_app.config['APP_CONFIG']
    with connect_database(config.DB_FILE) as conn:
        data = get_by_type(conn, Types.PROMPT)

    prompts = []
    for d in data:
        prompts.append({
            "id": d['id'],
            "prompt": d['prompt']
        })
    
    return {"prompts": prompts}

@bp.route('/api/res/form/prompt', methods=['POST'])
def post_form_prompt ():
    """
    プロンプトを新規保存する。
    """
    config = current_app.config['APP_CONFIG']
    try:
        form = PromptData(**request.json)
    except ValidationError as e:
        return {'error': e.errors()}, 400

    with connect_database(config.DB_FILE) as conn:
        insert(conn, Types.PROMPT, form.prompt)
        conn.commit()

    return {"status": "OK"}

@bp.route('/api/res/form/negative_prompt', methods=['GET'])
def get_form_negative_prompt ():
    """
    ネガティブプロンプトを取得する。
    """
    config = current_app.config['APP_CONFIG']
    with connect_database(config.DB_FILE) as conn:
        data = get_by_type(conn, Types.NEGATIVE_PROMPT)

    prompts = []
    for d in data:
        prompts.append({
            "id": d['id'],
            "prompt": d['prompt']
        })
    
    return {"prompts": prompts}

@bp.route('/api/res/form/negative_prompt', methods=['POST'])
def post_form_negative_prompt ():
    """
    ネガティブプロンプトを保存する。
    """
    config = current_app.config['APP_CONFIG']
    try:
        form = PromptData(**request.json)
    except ValidationError as e:
        return {'error': e.errors()}, 400

    with connect_database(config.DB_FILE) as conn:
        insert(conn, Types.NEGATIVE_PROMPT, form.prompt)
        conn.commit()

    return {"status": "OK"}

@bp.route('/api/res/form/prompt/<int:id>', methods=['POST'])
def post_form_prompt_id (id:int):
    """
    プロンプトを更新する。
    今の所更新日付を更新するだけ。
    つまり並び順の変更。
    """
    config = current_app.config['APP_CONFIG']
    with connect_database(config.DB_FILE) as conn:
        update(conn, id)
        conn.commit()

    return {"status": "OK"}


@bp.route('/api/res/form/prompt/<int:id>', methods=['DELETE'])
def delete_form_prompt (id:int):
    """
    プロンプトを削除する。
    """
    config = current_app.config['APP_CONFIG']
    with connect_database(config.DB_FILE) as conn:
        delete(conn, id)
        conn.commit()

    return {"status": "OK"}
