""" ワーカープロセスに指示を出すためのAPIを提供する
"""
from flask import Blueprint

from yt_diffuser.web.connection import get_shared_conn

worker_bp = Blueprint('api_worker', __name__)

@worker_bp.route('/api/worker/download', methods=['POST'])
def download ():
    """ ワーカープロセスに指示を出す
    """
    conn = get_shared_conn()
    conn.send(('download', None))
    return 'ok'