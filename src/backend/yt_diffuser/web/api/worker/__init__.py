""" ワーカープロセスに指示を出すためのAPIを提供する
"""
from flask import Blueprint

from yt_diffuser.web.worker_sender import get_send_queue

worker_bp = Blueprint('api_worker', __name__)

@worker_bp.route('/api/worker/download', methods=['POST'])
def download ():
    """ モデルダウンロード
    """
    q = get_send_queue()
    q.put(('download', None))
    return {'status': 'ok'}

@worker_bp.route('/api/worker/stop', methods=['GET'])
def stop ():
    """ 処理中断
    """
    q = get_send_queue()
    q.put(('stop', None))
    return {'status': 'ok'}