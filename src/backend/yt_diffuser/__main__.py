""" ゆとりでふーざー メインモジュール

Web APIプロセスのメイン処理
"""
import sys
import os
import logging; logger = logging.getLogger('yt_diffuser')

import uvicorn

if __name__ == '__main__':   # pragma: no cover
    if os.environ.get('DEBUG') == '1':
        logger.setLevel(level=logging.DEBUG)

    uvicorn.run("yt_diffuser.adapters.web.app:create_app", host="0.0.0.0", port=8000, reload=True)