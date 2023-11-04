"""sse関連のAPIモジュール
"""
from logging import getLogger; logger = getLogger(__name__)
from flask import Blueprint, Response
import asyncio
import time

from yt_diffuser.web.worker_listener import subscribe, unsubscribe, Subscriber, get_latest_message

sse_bp = Blueprint('api_res_sse', __name__)

@sse_bp.route('/api/sse/status', methods=['GET'])
def get_status ():
    """プロセスの状態を取得する
    """

    status = get_latest_message('status')

    def receiver(data):
        """ メッセージ受信コールバック
        """
        nonlocal status
        status = data

    subscriber = Subscriber()
    subscribe('status', subscriber)
    if status is None:
        status = ''

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

            try:
                status = subscriber.queue.get_nowait()
            except asyncio.QueueEmpty:
                pass

            yield f"data: {status}\n\n"
            time.sleep(1)

    except GeneratorExit:
        unsubscribe('status', subscriber)
