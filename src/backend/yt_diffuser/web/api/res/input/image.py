"""
i2i、InPaint、ControlNetの入力画像を受け取るAPI
"""
import logging; logger = logging.getLogger(__name__)
import os
from pathlib import Path

from flask import (
    Blueprint,
    current_app,
    request
)

from yt_diffuser.config import AppConfig

bp = Blueprint('api_res_input_image', __name__)

@bp.route('/api/res/input/image/<image_type>', methods=['POST'])
def upload_image(image_type:str):
    """
    inputディレクトリに画像を保存する
    """
    if image_type not in ['source', 'mask', 'controlnet']:
        return 'not found', 404

    config:AppConfig = current_app.config['APP_CONFIG']
    upload_file = request.files['image']
    upload_file_ext = Path(upload_file.filename).suffix

    if upload_file_ext != '.png':
        return 'invalid file type', 400

    filepath = None
    if image_type == 'mask':
        filepath = config.INPUT_MASK_FILE
    elif image_type == 'controlnet':
        filepath = config.INPUT_CONTROLNET_FILE
    else:
        filepath = config.INPUT_SOURCE_FILE

    filepath.parent.mkdir(parents=True, exist_ok=True)
    upload_file.save(filepath)
        
    return 'ok', 200


@bp.route('/api/res/input/image/<image_type>', methods=['DELETE'])
def delete_image(image_type:str):
    """
    inputディレクトリの画像を削除する
    """
    if image_type not in ['source', 'mask', 'controlnet']:
        return 'not found', 404

    config:AppConfig = current_app.config['APP_CONFIG']
    filepath = None
    if image_type == 'mask':
        filepath = config.INPUT_MASK_FILE
    elif image_type == 'controlnet':
        filepath = config.INPUT_CONTROLNET_FILE
    else:
        filepath = config.INPUT_SOURCE_FILE
    
    if filepath.exists():
        filepath.unlink()
        return 'ok', 200
    else:
        return 'not found', 404