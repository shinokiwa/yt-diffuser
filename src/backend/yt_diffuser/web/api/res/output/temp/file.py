"""
一時保存リソース関係のAPI
/temp/以下のファイルの場合

- GET: ファイルの情報を取得する。
- POST: ファイルを正式に保存する。
- DELETE: ファイルを削除する。
"""
from flask import Blueprint, current_app, request
from pydantic import ValidationError

from yt_diffuser.config import AppConfig
from yt_diffuser.web.api.res.output.temp.utils import PostTempRequest, get_temp_file_path
from yt_diffuser.utils.event import FilesystemEvent


bp = Blueprint('api_res_output_temp_file', __name__)

@bp.route('/api/res/output/temp/<path:subpath>', methods=['GET'])
def get_temp_file (subpath:str):
    """
    一時保存リソースの情報を取得する。
    現在未実装
    """
    config:AppConfig = current_app.config['APP_CONFIG']
    base_dir = config.OUTPUT_TEMP_DIR

    try:
        request_file = get_temp_file_path(base_dir, subpath)
    except ValueError as e:
        return {'status': 'ng', 'message': 'invalid-request', 'detail': str(e)}, 400
    
    # ファイルの情報を取得
    # ここから未実装
    return {'status': 'ok'}


@bp.route('/api/res/output/temp/<path:subpath>', methods=['POST'])
def post_temp_file (subpath:str):
    """
    一時保存リソースを正式に保存する。

    実態としてはファイルの移動。
    """
    config:AppConfig = current_app.config['APP_CONFIG']
    base_dir = config.OUTPUT_TEMP_DIR
    target_base_dir = config.OUTPUT_IMAGE_DIR

    try:
        postTempRequest = PostTempRequest(**request.json)
        full_target = postTempRequest.get_full_target(target_base_dir)
        request_file = get_temp_file_path(base_dir, subpath)
    except ValidationError as e:
        return {'status': 'ng', 'message': 'invalid-request', 'detail': e.errors()}, 400
    except ValueError as e:
        return {'status': 'ng', 'message': 'invalid-path', 'detail': str(e)}, 400

    full_target.mkdir(parents=True, exist_ok=True)

    # ファイルを正式に保存
    new_path = request_file.rename(full_target / request_file.name)

    FilesystemEvent.send(FilesystemEvent.Type.DELETE, str(request_file))
    FilesystemEvent.send(FilesystemEvent.Type.CREATE, str(new_path))

    return {'status': 'ok'}


@bp.route('/api/res/output/temp/<path:subpath>', methods=['DELETE'])
def delete_temp_file (subpath:str):
    """
    一時保存リソースを削除する。
    """
    config:AppConfig = current_app.config['APP_CONFIG']
    base_dir = config.OUTPUT_TEMP_DIR

    try:
        request_file = get_temp_file_path(base_dir, subpath)
    except ValueError as e:
        return {'status': 'ng', 'message': 'invalid-path', 'detail': str(e)}, 400
    
    # ファイルを削除
    request_file.unlink(missing_ok=True)
    FilesystemEvent.send(FilesystemEvent.Type.DELETE, str(request_file))

    return {'status': 'ok'}