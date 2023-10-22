"""sse関連のAPIモジュール
"""
from flask import Blueprint, Response, request, abort, current_app
import json

sse_bp = Blueprint('api_sse', __name__)


def status_stream():
    """プロセスの状態を取得する
    """
    import time
    from datetime import datetime

    while True:
        # 暫定で現在時刻を返す
        time.sleep(1)
        data = {}
        data['status'] = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        yield f"data: {json.dumps(data)}\n\n"

@sse_bp.route('/sse/status', methods=['GET'])
def get_status ():
    """プロセスの状態を取得する
    """
    return Response(status_stream(), mimetype='text/event-stream')