"""sse関連のAPIモジュール
"""
import json
from logging import getLogger; logger = getLogger(__name__)
from flask import Blueprint, Response

from yt_diffuser.web.worker_listener import get_listener, remove_listener, Empty

sse_download_bp = Blueprint('api_res_sse_download', __name__)

@sse_download_bp.route('/api/sse/download', methods=['GET'])
def get_download ():
    """ ダウンロードの状態を取得する
    """
    return Response(status_stream(), mimetype='text/event-stream')

def status_stream():
    """プロセスの状態を取得する
    """
    data = {}
    queue = get_listener('download')

    try:
        while True:
            try:
                data = queue.get(timeout=5)
            except Empty:
                pass

            yield f"data: {json.dumps(data)}\n\n"

    except GeneratorExit:
        remove_listener('download', queue)
