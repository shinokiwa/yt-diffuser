"""
画像を生成するAPI
"""
from flask import Blueprint, current_app, request
from pydantic import ValidationError

from yt_diffuser.config import AppConfig
from yt_diffuser.web.process.generate_image import is_running, text_to_image ,image_to_image, inpaint
from yt_diffuser.workers.generate_image.tasks.validations import TextToImageRequest, ImageToImageRequest

bp = Blueprint('api_generate_preview', __name__)

@bp.route('/api/generate/preview/text_to_image', methods=['POST'])
def process_t2i () -> str:
    """
    Text to Imageでプレビュー画像を生成する。

    Returns:
        str: "OK"
    """
    if not is_running():
        return "process is not running", 400

    config:AppConfig = current_app.config['APP_CONFIG']

    fixed_data = {
        "output_dir": str(config.OUTPUT_PREVIEW_PATH.parent),
        "filename": str(config.OUTPUT_PREVIEW_PATH.name),
        "generate_count": 1
    }

    req_data = {**request.json, **fixed_data}

    try:
        data = TextToImageRequest(**req_data).dict()
    except ValidationError as e:
        return str(e), 400

    config.OUTPUT_PREVIEW_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    text_to_image(data)
    return "OK"

@bp.route('/api/generate/preview/image_to_image', methods=['POST'])
def process_i2i () -> str:
    """
    Image to Imageでプレビュー画像を生成する。

    Returns:
        str: "OK"
    """
    if not is_running():
        return "process is not running", 400

    config:AppConfig = current_app.config['APP_CONFIG']

    fixed_data = {
        "output_dir": str(config.OUTPUT_PREVIEW_PATH.parent),
        "filename": str(config.OUTPUT_PREVIEW_PATH.name),
        "generate_count": 1
    }

    req_data = {**request.json, **fixed_data}

    try:
        data = ImageToImageRequest(**req_data).dict()
    except ValidationError as e:
        return str(e), 400

    config.OUTPUT_PREVIEW_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    image_to_image(data)
    return "OK"

@bp.route('/api/generate/preview/inpaint', methods=['POST'])
def process_inpaint () -> str:
    """
    InPaintでプレビュー画像を生成する。

    Returns:
        str: "OK"
    """
    if not is_running():
        return "process is not running", 400

    config:AppConfig = current_app.config['APP_CONFIG']

    fixed_data = {
        "output_dir": str(config.OUTPUT_PREVIEW_PATH.parent),
        "filename": str(config.OUTPUT_PREVIEW_PATH.name),
        "generate_count": 1
    }

    req_data = {**request.json, **fixed_data}

    try:
        data = ImageToImageRequest(**req_data).dict()
    except ValidationError as e:
        return str(e), 400

    config.OUTPUT_PREVIEW_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    inpaint(data)
    return "OK"