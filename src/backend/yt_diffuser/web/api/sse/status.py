"""sse関連のAPIモジュール
"""
from logging import getLogger; logger = getLogger(__name__)
from flask import Blueprint, Response

from yt_diffuser.web.worker_listener import get_listener, remove_listener, Empty

sse_status_bp = Blueprint('api_res_sse_status', __name__)

@sse_status_bp.route('/api/sse/status', methods=['GET'])
def get_status ():
    """プロセスの状態を取得する
    """
    return Response(status_stream(), mimetype='text/event-stream')

def status_stream():
    """プロセスの状態を取得する
    """
    status = ''
    queue = get_listener('status')

    try:
        while True:
            try:
                status = queue.get(timeout=5)
            except Empty:
                pass

            yield f"data: {status}\n\n"

    except GeneratorExit:
        remove_listener('status', queue)
