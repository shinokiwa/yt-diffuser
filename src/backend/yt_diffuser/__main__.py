""" ゆとりでふーざー メインモジュール

Web APIプロセスのメイン処理
"""
import sys
import os
import logging; logger = logging.getLogger('yt_diffuser')
logging.basicConfig(stream=sys.stdout)

from yt_diffuser.api.main import main

if __name__ == '__main__':   # pragma: no cover
    if os.environ.get('DEBUG') == '1':
        logger.setLevel(level=logging.DEBUG)
    main()