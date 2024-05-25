""" ゆとりでふーざー メインモジュール

Web APIプロセスのメイン処理
"""
import sys
import os
import logging; logger = logging.getLogger('yt_diffuser')
logging.basicConfig(stream=sys.stdout)

from yt_diffuser.config import AppConfig
from yt_diffuser.main import main
from yt_diffuser.dev_watcher import watchdog_process

if __name__ == '__main__':   # pragma: no cover
    if os.environ.get('DEBUG') == '1':
        logger.setLevel(level=logging.DEBUG)
        watchdog_process()
        main(AppConfig(
            debug=True
        ))

    else:
        main(AppConfig())