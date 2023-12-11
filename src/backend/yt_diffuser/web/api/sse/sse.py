"""sse関連のAPIモジュール
短いのでまとめる
"""
import json
from logging import getLogger; logger = getLogger(__name__)

from flask import Blueprint, Response

from yt_diffuser.web.api.sse.utils import event_stream

bp = Blueprint('api_res_sse_download', __name__)

@bp.route('/api/sse/download', methods=['GET'])
def get_download ():
    """ ダウンロードの状態を取得する
    """
    return Response(event_stream('download'), mimetype='text/event-stream')

@bp.route('/api/sse/status', methods=['GET'])
def get_status ():
    """プロセスの状態を取得する
    """
    return Response(event_stream('status'), mimetype='text/event-stream')

@bp.route('/api/sse/message', methods=['GET'])
def get_message ():
    """ ワーカープロセスからのメッセージを取得する
    """
    return Response(event_stream('message'), mimetype='text/event-stream')