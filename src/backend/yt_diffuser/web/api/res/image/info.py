"""
画像のプロンプト情報を取得するAPI
"""
# まだコピーしてきただけ

import os, logging
logger = logging.getLogger(__name__)

from flask import request
from werkzeug.utils import secure_filename
from PIL import Image

from yt_stablediffusion import path
from .response import APIResponse

def api_get_image_info(filepath:str):
    """指定した画像の情報を取得するAPI

    Args:
        imagefile (str): 画像ファイル、セキュリティのため/userdata/始まりのみ受け付ける。

    Returns:
        _type_: _description_
    """
    res = APIResponse()

    if filepath.startswith('userdata/') == False or '/../' in filepath:
        return res.err_validation(errors=["Invalid file path."])
    
    imagefile = filepath[len('userdata/'):]
    target_file = path.join(path.user_dir, imagefile)
    logger.debug(f'Reading file info : {target_file}')

    if path.isfile(target_file) == False:
        return res.err_validation(errors=["Imagefile not found."])

    im = Image.open(target_file)
    text = im.text
    result = {}
    if 'Title' in text: result['Title'] = text.get('Title')
    if 'Description' in text: result['Description'] = text.get('Description')
    if 'Software' in text: result['Software'] = text.get('Software')
    if 'Source' in text: result['Source'] = text.get('Source')
    if 'Comment' in text: result['Comment'] = text.get('Comment')

    return res.ok(data=result)
