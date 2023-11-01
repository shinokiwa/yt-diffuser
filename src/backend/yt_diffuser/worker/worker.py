""" ワーカーの処理を振り分ける

一部の処理については、実行可能かどうかに条件がある。
"""
from logging import getLogger; logger = getLogger(__name__)

from yt_diffuser.worker.connection import get_shared_conn

def dispatch (event:str, data = None):
    logger.debug('dispatch: event=%s', event)
    if event == "download":
        conn = get_shared_conn()
        from datetime import datetime
        conn.send(('status', datetime.now().strftime('%Y/%m/%d %H:%M:%S')))
        
    elif event == "stop_download":
        pass
    elif event == "load":
        pass
    elif event == "generate":
        pass
    elif event == "stop_generate":
        pass