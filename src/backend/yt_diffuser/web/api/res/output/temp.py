"""
一時保存リソース関係のAPI

- /temp/へのアクセスの場合、メソッドごとに以下のような処理を行う。
    - GET: 一時保存中のファイル一覧を取得する。
        - SSEでストリームで返し、その後も更新があるたびに追加で返す。
    - POST: 全ての一次保存中ファイルを正式に保存する。
    - DELETE: 全ての一時保存中ファイルを削除する。
- /temp/以下のファイルの場合、メソッドごとに以下のような処理を行う。
    - GET: ファイルの情報を取得する。
    - POST: ファイルを正式に保存する。
    - DELETE: ファイルを削除する。
"""
import shutil
from pathlib import Path
from datetime import datetime

from flask import Blueprint, current_app, Response, request
from pydantic import BaseModel, ValidationError, Field

from yt_diffuser.config import AppConfig
from yt_diffuser.web.api.res.output.utils import stream_list, is_child

bp = Blueprint('api_res_output_temp', __name__)


class PostTempRequest(BaseModel):
    """
    一時保存中のファイルを正式に保存するリクエスト
    """
    target: str = Field(default_factory=lambda: datetime.now().strftime('%Y-%m-%d %H-%M-%S'))

    def get_full_target (self, base_dir:Path):
        """
        ターゲットのフルパスを取得する。
        
        raise:
            ValidationError: ターゲットがベースディレクトリより上にある場合
        """
        target = Path(self.target)
        full_target = (base_dir / target).resolve()

        if not is_child(base_dir, full_target):
            raise ValidationError('invalid target', self)
        
        return full_target


def get_temp_file_path (base_dir:Path, subpath:str):
    """
    subpathから一時保存中ファイルのフルパスを取得する。
    共通チェックも兼ねる。

    raise:
        ValidationError: ファイルが存在しない場合、ファイルでない場合
    """
    request_file = (base_dir / subpath).resolve()

    # ファイルが存在しない場合はエラー
    # ファイルでない場合はエラー
    # subpathがベースディレクトリより上にある場合はエラー
    if not request_file.exists() \
        or not request_file.is_file() \
        or not is_child(base_dir, request_file):
        raise ValueError('invalid path')

    return request_file


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
        file.rename(full_target / file.name)

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

    return {'status': 'ok'}


@bp.route('/api/res/output/temp/<path:subpath>', methods=['GET'])
def get_temp_file (subpath:str):
    """
    画像リソースの情報を取得する。
    現在未実装
    """
    config:AppConfig = current_app.config['APP_CONFIG']
    base_dir = config.OUTPUT_TEMP_DIR

    try:
        request_file = get_temp_file_path(base_dir, subpath)
    except ValidationError as e:
        return {'status': 'ng', 'message': 'invalid-request', 'detail': e.errors()}, 400
    
    # ファイルの情報を取得
    # ここから未実装
    return {'status': 'ok'}


@bp.route('/api/res/output/temp/<path:subpath>', methods=['POST'])
def post_temp_file (subpath:str):
    """
    画像リソースを正式に保存する。

    実態としてはファイルの移動。
    """
    config:AppConfig = current_app.config['APP_CONFIG']
    base_dir = config.OUTPUT_TEMP_DIR
    target_base_dir = config.OUTPUT_IMAGE_DIR

    try:
        request_file = get_temp_file_path(base_dir, subpath)
        postTempRequest = PostTempRequest(**request.json)
        full_target = postTempRequest.get_full_target(target_base_dir)
    except ValidationError as e:
        return {'status': 'ng', 'message': 'invalid-request', 'detail': e.errors()}, 400

    # ファイルを正式に保存
    request_file.rename(full_target / request_file.name)

    return {'status': 'ok'}


@bp.route('/api/res/output/temp/<path:subpath>', methods=['DELETE'])
def delete_temp_file (subpath:str):
    """
    一次保存リソースを削除する。
    """
    config:AppConfig = current_app.config['APP_CONFIG']
    base_dir = config.OUTPUT_TEMP_DIR

    try:
        request_file = get_temp_file_path(base_dir, subpath)
    except ValidationError as e:
        return {'status': 'ng', 'message': 'invalid-request', 'detail': e.errors()}, 400
    
    # ファイルを削除
    request_file.unlink(missing_ok=True)

    return {'status': 'ok'}