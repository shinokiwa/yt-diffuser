"""sse関連のAPIモジュール
"""
from logging import getLogger; logger = getLogger(__name__)
from flask import Blueprint, Response
import json

from yt_diffuser.web.worker_listener import get_listener, remove_listener, Empty

sse_progress_bp = Blueprint('api_res_sse_progress', __name__)

@sse_progress_bp.route('/api/sse/progress', methods=['GET'])
def get_status ():
    """ ワーカープロセスの進捗状態を取得する
    """
    return Response(progress_stream(), mimetype='text/event-stream')

def progress_stream():
    """ ワーカープロセスの進捗状態を取得する
    """
    progress = ''
    queue = get_listener('progress')

    try:
        while True:
            try:
                progress = queue.get(timeout=5)
                progress = json.dumps(progress)
            except Empty:
                pass

            yield f"data: {progress}\n\n"

    except GeneratorExit:
        remove_listener('status', queue)
