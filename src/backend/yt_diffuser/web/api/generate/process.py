"""
生成プロセス制御関係のAPI
"""
from flask import Blueprint, current_app, request
from pydantic import BaseModel, ValidationError

from yt_diffuser.config import AppConfig
from yt_diffuser.web.process.generate_image import (
    is_running,
    load,
    terminate,
    remove_lora,
    compile
)

bp = Blueprint('api_generate_process', __name__)

class LoadRequest(BaseModel):
    model_name: str
    revision: str
    compile: int = 0

@bp.route('/api/generate/process/load', methods=['POST'])
def process_load () -> str:
    """
    画像生成プロセスを開始する。
    画像生成プロセスは１つしか実行されない。

    Returns:
        str: "OK"
    """
    if is_running():
        terminate()

    try:
        req = LoadRequest(**request.json)
    except ValidationError as e:
        return str(e), 400

    load(
        current_app.config['APP_CONFIG'],
        model_name=req.model_name,
        revision=req.revision,
        compile=req.compile == 1
    )
    return "OK"


@bp.route('/api/generate/process/terminate', methods=['GET'])
def process_terminate () -> str:
    """
    画像生成プロセスを終了する。

    Returns:
        str: "OK"
    """
    if not is_running():
        return "process is not running", 400

    terminate()
    return "OK"

@bp.route('/api/generate/process/lora/load', methods=['POST'])
def process_lora_load () -> str:
    """
    LORAをロードする。
    未実装。

    Returns:
        str: "OK"
    """
    if not is_running():
        return "process is not running", 400

    return "OK"

@bp.route('/api/generate/process/lora/remove', methods=['GET'])
def process_lora_remove () -> str:
    """
    ロード済みのLORAを解放する。

    Returns:
        str: "OK"
    """
    if not is_running():
        return "process is not running", 400
    
    remove_lora()

    return "OK"

@bp.route('/api/generate/process/compile', methods=['GET'])
def process_compile () -> str:
    """
    モデルをコンパイルする。

    Returns:
        str: "OK"
    """
    if not is_running():
        return "process is not running", 400

    compile()
    return "OK"