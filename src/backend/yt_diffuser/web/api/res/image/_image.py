"""
画像リソース関係のAPI
"""
import os
from pathlib import Path
import time

from flask import Blueprint, current_app, Response

from yt_diffuser.config import AppConfig
from yt_diffuser.store import connect_database

bp = Blueprint('api_res_image', __name__)

@bp.route('/api/res/image/list/', defaults={'subpath': ''})
@bp.route('/api/res/image/list/<path:subpath>', methods=['GET'])
def get_image_list (subpath:str):
    """
    画像リソースの一覧を取得する。

    - list以降のパスは、画像を格納しているディレクトリのパスを表す。
    - list以降に何も指定しない場合、すべてのディレクトリの画像を取得する。
    - 出力はstreamで行う。
    """
    config:AppConfig = current_app.config['APP_CONFIG']
    base_dir = config.OUTPUT_IMAGE_DIR

    request_path = (base_dir / subpath).resolve()

    # subpathがベースディレクトリより上にある場合はエラー
    if request_path != base_dir and not base_dir in request_path.parents:
        return 'invalid path', 400

    # ディレクトリが存在しない場合はエラー
    if not request_path.exists():
        return 'invalid path', 400
    
    # ディレクトリでない場合はエラー
    if not request_path.is_dir():
        return 'invalid path', 400
    
    # ディレクトリ内のファイル一覧を取得
    return Response(stream_list(request_path), mimetype='text/event-stream')


def stream_list (path:Path):
    """
    ファイル一覧をstreamで返す。

    - ファイル一覧は指定したパスからの相対パスで返す。
    """
    for root, dirs, files in os.walk(path):
        for file in files:
            full_path = Path(root) / file
            yield 'data: ' + str(full_path.relative_to(path)) + '\n\n'
    
    while True:
        time.sleep(20)
        yield 'data: \n\n'