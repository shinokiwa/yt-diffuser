""" Server-Sent Events 関連のモジュール用ユーティリティ
"""
from typing import Generator
import json

from yt_diffuser.web.message_listener import get_event_listener, remove_event_listener, Empty


def event_stream(event:str, timeout:float=20.0) -> Generator[str, None, None]:
    """
    メッセージリスナーからのメッセージを取得し、データを文字列として返す。

    - データはSSE向けに data: value\n\n の形式になる。
    - データが辞書型だった場合、JSONを文字列化した形式になる。
    - SSEのタイムアウトを回避するため、20秒間データがなかった場合は空(data: \n\n)のデータを返す。
    - GeneratorExitが発生した場合、メッセージリスナーから削除する。

    Args:
        event (str): イベント名

    Yields:
        Str: イベントデータ
    """
    queue = get_event_listener(event)

    try:
        while True:
            try:
                data = queue.get(timeout=timeout)
                if type(data) == dict:
                    data = json.dumps(data)
            except Empty:
                data = ""

            yield f"data: {data}\n\n"

    except GeneratorExit:
        remove_event_listener(event, queue)