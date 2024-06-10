"""
プレビュー関係のAPI

- GET: プレビュー画像を取得する。
    - SSEでストリームで返し、その後も更新があるたびに追加で返す。
- DELETE: プレビュー画像を削除する。
"""
from flask import Blueprint, current_app, Response

from yt_diffuser.config import AppConfig
from yt_diffuser.web.api.res.output.utils import stream_list

bp = Blueprint('api_res_output_temp_dir', __name__)

@bp.route('/api/res/output/preview', methods=['GET'])
def get_preview ():
    """
    一時保存中のファイル一覧を取得する。
    """
    config:AppConfig = current_app.config['APP_CONFIG']
    base_dir = config.OUTPUT_PREVIEW_PATH.parent

    base_dir.mkdir(parents=True, exist_ok=True)

    return Response(stream_list(base_dir), mimetype='text/event-stream')