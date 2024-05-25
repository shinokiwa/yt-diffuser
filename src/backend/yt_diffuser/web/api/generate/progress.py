"""
生成ワーカーのステータスを返すSSE
"""
from typing import Generator
import json
from logging import getLogger; logger = getLogger(__name__)

from flask import Blueprint, Response

from yt_diffuser.utils.event import GenerateProgressEvent, Empty

bp = Blueprint('api_generate_progress', __name__)

@bp.route('/api/generate/progress', methods=['GET'])
def get_status ():
    """
    生成ワーカーの進捗状況を返すSSE
    """
    return Response(event_stream(), mimetype='text/event-stream')

def event_stream(timeout:float=5.0) -> Generator[str, None, None]:
    """
    メッセージリスナーからのメッセージを取得し、データを文字列として返す。

    - データはSSE向けに data: value\n\n の形式になる。
    - データは辞書型が前提。
    - SSEのタイムアウトを回避するため、5秒間データがなかった場合は空(data: \n\n)のデータを返す。
    - GeneratorExitが発生した場合、メッセージリスナーから削除する。

    Args:
        timeout (float, optional): 1回のデータ取得のタイムアウト秒数。これを超えるとkeep-aliveを返す。デフォルトは5.0。

    Yields:
        Str: イベントデータ
    """
    queue = GenerateProgressEvent.get_listener()

    try:
        while True:
            response = ""
            try:
                data_dict = queue.get(timeout=timeout)
                data_str = json.dumps(data_dict)
                
                response = f"data: {data_str}\n\n"
            except Empty:
                response = ": keep-alive\n\n"

            yield response

    except GeneratorExit:
        GenerateProgressEvent.remove_listener(queue)