""" ゆとりでふーざー メインモジュール

マスタープロセスとして起動し、Webモジュールとデータ処理モジュールを子プロセスとして起動、監視する。
"""
from logging import getLogger; logger = getLogger(__name__)

import os

from .main.process_manager import start_all
from .main.watchdog import watchdog_process

from .web.main import web_procedure
from yt_diffuser.worker.main import worker_procedure

if __name__ == '__main__':
    import logging; logging.basicConfig(level=logging.DEBUG)
    logger.debug("Start yt_diffuser")

    if os.environ.get('DEBUG') == '1':
        watchdog_process(procedure=start_all, args=(web_procedure, worker_procedure))
    else:
        start_all(web_procedure, worker_procedure)
