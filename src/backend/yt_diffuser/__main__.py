""" ゆとりでふーざー メインモジュール

マスタープロセスとして起動し、Webモジュールとデータ処理モジュールを子プロセスとして起動、監視する。
"""
from logging import getLogger; logger = getLogger(__name__)

import os

from yt_diffuser.store.db.setup import setup_database
from yt_diffuser.main.process_manager import start_loop
from yt_diffuser.main.watchdog import watchdog_process

if __name__ == '__main__':
    import logging; logging.basicConfig(level=logging.DEBUG)
    logger.debug("Start yt_diffuser")

    setup_database()

    if os.environ.get('DEBUG') == '1':
        watchdog_process(procedure=start_loop)
    else:
        start_loop()
