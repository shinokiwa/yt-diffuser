""" ワーカープロセスに指示を出すためのAPIを提供する
"""
from flask import Blueprint

from yt_diffuser.web.worker_sender import get_send_queue

worker_bp = Blueprint('api_worker', __name__)

@worker_bp.route('/api/worker/download', methods=['POST'])
def download ():
    """ ワーカープロセスに指示を出す
    """
    q = get_send_queue()
    q.put(('download', None))
    return 'ok'