""" ワーカーの処理を振り分ける

一部の処理については、実行可能かどうかに条件がある。
"""
from logging import getLogger; logger = getLogger(__name__)

from yt_diffuser.worker.web_sender import get_send_queue

def dispatch (msg):
    (event, data) = msg
    logger.debug('dispatch: event=%s', event)

    if event == "download":
        queue = get_send_queue()
        from datetime import datetime
        queue.put(('status', datetime.now().strftime('%Y/%m/%d %H:%M:%S')))
        
    elif event == "stop_download":
        pass
    elif event == "load":
        pass
    elif event == "generate":
        pass
    elif event == "stop_generate":
        pass