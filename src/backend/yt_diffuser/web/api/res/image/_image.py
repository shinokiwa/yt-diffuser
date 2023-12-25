"""
画像リソース関係のAPI
"""
from typing import Generator
import os
import json
from pathlib import Path

from flask import Blueprint, current_app, Response

from yt_diffuser.config import AppConfig
from yt_diffuser.store import connect_database
from yt_diffuser.web.message_listener import get_event_listener, remove_event_listener, Empty

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
    base_dir = config.OUTPUT_DIR

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


def stream_list (path:Path, timeout:float=20.0) -> Generator[str, None, None]:
    """
    ファイル一覧をstreamで返す。

    - ファイル一覧は指定したパスからの相対パスで返す。
    """
    try:
        data = {'type': 'list', 'target': None}
        for root, dirs, files in os.walk(path):
            for file in files:
                full_path = Path(root) / file
                data['target'] = str(full_path.relative_to(path))
                _data = json.dumps(data)
                yield f"data: {_data}\n\n"            
        
        queue = get_event_listener('file')

        while True:
            try:
                data = queue.get(timeout=timeout)
                if type(data) == dict:
                    event_path = Path(data['target'])
                    if event_path != path and not path in event_path.parents:
                        continue

                    data['target'] = str(event_path.relative_to(path))
                    data = json.dumps(data)
            except Empty:
                data = ""

            yield f"data: {data}\n\n"            
    except GeneratorExit:
        pass