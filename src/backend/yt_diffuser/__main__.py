""" ゆとりでふーざー メインモジュール

Web APIプロセスのメイン処理
"""
import os
import logging; logger = logging.getLogger('yt_diffuser')

from yt_diffuser.config import AppConfig
from yt_diffuser.main import main
from yt_diffuser.dev_watcher import watchdog_process

if __name__ == '__main__':   # pragma: no cover
    if os.environ.get('DEBUG') == '1':
        config = AppConfig(
            debug=True
        )

        watchdog_process(main, (config,))
    else:
        main(AppConfig())