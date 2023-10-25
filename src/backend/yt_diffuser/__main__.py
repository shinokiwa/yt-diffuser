""" ゆとりでふーざー メインモジュール

マスタープロセスとして起動し、Webモジュールとデータ処理モジュールを子プロセスとして起動、監視する。
"""
from logging import getLogger; logger = getLogger(__name__)

import os

from .main.main import process
from .main.watchdog import watchdog_process

from .web.main import web_procedure
from .processing.main import processing_process

if __name__ == '__main__':
    import logging; logging.basicConfig(level=logging.DEBUG)
    logger.debug("Start yt_diffuser")

    if os.environ.get('DEBUG') == '1':
        logger.debug("Debugmode on")
        watchdog_process(main=process, web_main=web_procedure, processing_main=processing_process)
    else:
        process(web_main=web_procedure, processing_main=processing_process)
