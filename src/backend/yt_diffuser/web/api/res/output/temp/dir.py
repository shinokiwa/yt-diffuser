"""
一時保存リソース関係のAPI
/temp/へのアクセスの場合

- GET: 一時保存中のファイル一覧を取得する。
    - SSEでストリームで返し、その後も更新があるたびに追加で返す。
- POST: 全ての一次保存中ファイルを正式に保存する。
- DELETE: 全ての一時保存中ファイルを削除する。
"""
import shutil

from flask import Blueprint, current_app, Response, request
from pydantic import ValidationError

from yt_diffuser.config import AppConfig
from yt_diffuser.web.api.res.output.utils import stream_list
from yt_diffuser.web.api.res.output.temp.utils import PostTempRequest
from yt_diffuser.utils.event import FilesystemEvent

bp = Blueprint('api_res_output_temp_dir', __name__)

@bp.route('/api/res/output/temp', methods=['GET'])
def get_temp ():
    """
    一時保存中のファイル一覧を取得する。
    """
    config:AppConfig = current_app.config['APP_CONFIG']
    base_dir = config.OUTPUT_TEMP_DIR

    base_dir.mkdir(parents=True, exist_ok=True)

    return Response(stream_list(base_dir), mimetype='text/event-stream')


@bp.route('/api/res/output/temp', methods=['POST'])
def post_temp ():
    """
    全ての一時保存中ファイルを正式に保存する。

    - リクエストボディはJSON形式で、以下のフィールドを含む。
        - target: 保存先のディレクトリ
    - 一次保存ディレクトリが存在しない場合は何もせずに終了する。
    - 一次保存ディレクトリが空の場合は何もせずに終了する。
    - 保存先のディレクトリを指定しない場合、現在時刻で作成したディレクトリに保存する。
    """
    config:AppConfig = current_app.config['APP_CONFIG']
    base_dir = config.OUTPUT_TEMP_DIR
    if not base_dir.exists():
        return {'status': 'ok'}
    
    files = list(base_dir.glob('*'))
    if len(files) == 0:
        return {'status': 'ok'}
    
    try:
        postTempRequest = PostTempRequest(**request.json)
        full_target = postTempRequest.get_full_target(config.OUTPUT_IMAGE_DIR)
    except ValidationError as e:
        return {'status': 'ng', 'message': 'invalid-request', 'detail': e.errors()}, 400
    
    full_target.mkdir(parents=True, exist_ok=True)

    for file in files:
        old_name = str(file)
        file.rename(full_target / file.name)
        FilesystemEvent.send(FilesystemEvent.Type.DELETE, old_name)

    return {'status': 'ok'}


@bp.route('/api/res/output/temp', methods=['DELETE'])
def delete_temp ():
    """
    全ての一時保存中ファイルを削除する。
    """
    config:AppConfig = current_app.config['APP_CONFIG']
    base_dir = config.OUTPUT_TEMP_DIR

    if not base_dir.exists():
        return {'status': 'ok'}
    
    for path in base_dir.iterdir():
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink(missing_ok=True)
        FilesystemEvent.send(FilesystemEvent.Type.DELETE, str(path))

    return {'status': 'ok'}
