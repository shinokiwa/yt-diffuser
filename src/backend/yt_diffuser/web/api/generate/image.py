"""
画像を生成するAPI
"""
from flask import Blueprint, current_app, request
from pydantic import BaseModel, ValidationError

from yt_diffuser.config import AppConfig
from yt_diffuser.web.process.generate_image import is_running, load, text_to_image, terminate
from yt_diffuser.workers.generate_image.validations import TextToImageRequest

bp = Blueprint('api_generate_image', __name__)

class LoadRequest(BaseModel):
    model_name: str
    revision: str

@bp.route('/api/generate/image/load', methods=['POST'])
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

    load(current_app.config['APP_CONFIG'], req.model_name, req.revision)
    return "OK"


@bp.route('/api/generate/image/terminate', methods=['GET'])
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


@bp.route('/api/generate/image/text_to_image', methods=['POST'])
def process_generate () -> str:
    """
    Text to Imageで画像を生成する。

    Returns:
        str: "OK"
    """
    if not is_running():
        return "process is not running", 400

    config:AppConfig = current_app.config['APP_CONFIG']

    fixed_data = {
        "output_dir": str(config.OUTPUT_TEMP_DIR),
    }

    req_data = {**request.json, **fixed_data}

    try:
        data = TextToImageRequest(**req_data).dict()
    except ValidationError as e:
        return str(e), 400

    config.OUTPUT_TEMP_DIR.mkdir(parents=True, exist_ok=True)
    
    text_to_image(data)
    return "OK"
