"""
モデルダウンロードAPI
"""
from flask import Blueprint, current_app, request
from pydantic import BaseModel, ValidationError

from yt_diffuser.web.process.download import is_running, download, terminate

bp = Blueprint('api_download', __name__)

class DownloadRequest(BaseModel):
    """
    モデルダウンロードAPIのリクエスト
    """
    repo_id: str
    revision: str

@bp.route('/api/download/start', methods=['POST'])
def start ():
    """
    モデルダウンロード

    ダウンロードを実行する。
    リクエストボディはJSON形式で、以下のフィールドを含む。
    - repo_id: リポジトリID
    - revision: リビジョン
    既にダウンロードが実行中の場合は400エラーを返す。
    """
    if not request.is_json:
        return {'status': 'ng', 'message': 'invalid-json'}, 400
    
    try:
        request_data = DownloadRequest(**request.json).dict()
    except ValidationError as e:
        return {'status': 'ng', 'message': 'invalid-request', 'detail': e.errors()}, 400

    if is_running():
        return {'status': 'ng', 'message': 'download-running'}, 400

    download(
        config=current_app.config['APP_CONFIG'],
        repo_id=request_data['repo_id'],
        revision=request_data['revision']
    )
    return {'status': 'ok'}

@bp.route('/api/download/stop', methods=['GET'])
def stop ():
    """
    処理中断
    """
    terminate()
    return {'status': 'ok'}