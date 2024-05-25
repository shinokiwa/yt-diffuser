"""
画像リソース関係のAPI

- アクセス先がディレクトリかファイルかで処理が変わる。
- ディレクトリの場合、メソッドごとに以下のような処理を行う。
    - GET: ディレクトリ内のファイル一覧を取得する。
        - SSEでストリームで返し、その後も更新があるたびに追加で返す。
    - PUT: ディレクトリ内にファイルを保存する。
    - POST: ディレクトリの情報変更(リネーム)を行う。
    - DELETE: ディレクトリを配下のファイルごと削除する。
- ファイルの場合、メソッドごとに以下のような処理を行う。
    - GET: ファイルの情報を取得する。
    - PUT: ファイルを上書き保存する。
    - POST: ファイルの情報変更(リネーム)を行う。
    - DELETE: ファイルを削除する。
"""
from pathlib import Path

from flask import Blueprint, current_app, Response

from yt_diffuser.config import AppConfig
from yt_diffuser.database import connect_database

bp = Blueprint('api_res_output_image', __name__)

@bp.route('/api/res/output/image/list/', defaults={'subpath': ''})
@bp.route('/api/res/output/image/list/<path:subpath>', methods=['GET'])
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

