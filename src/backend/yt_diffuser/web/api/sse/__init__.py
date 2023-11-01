"""sse関連のAPIモジュール
"""
from logging import getLogger; logger = getLogger(__name__)
from flask import Blueprint, Response
from gevent import sleep
from gevent.queue import Empty

from yt_diffuser.web.worker_listener import subscribe, unsubscribe, Subscriber, get_latest_message

sse_bp = Blueprint('api_res_sse', __name__)

@sse_bp.route('/api/sse/status', methods=['GET'])
def get_status ():
    """プロセスの状態を取得する
    """
    return Response(status_stream(), mimetype='text/event-stream')

def status_stream():
    """プロセスの状態を取得する
    """

    subscriber = Subscriber()
    subscribe('status', subscriber)
    status = get_latest_message('status')
    if status is None:
        status = ''

    try:
        while True:
            subscriber.heartbeat()
            yield f"data: {status}\n\n"

            try:
                status = subscriber.queue.get(timeout=5)
            except Empty:
                pass


    except GeneratorExit:
        unsubscribe('status', subscriber)
