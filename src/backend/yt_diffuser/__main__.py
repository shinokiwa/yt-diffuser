""" ゆとりでふーざー メインモジュール

マスタープロセスとして起動し、Webモジュールとデータ処理モジュールを子プロセスとして起動、監視する。
"""
from logging import getLogger; logger = getLogger(__name__)

import os

from yt_diffuser.config import AppConfig
from yt_diffuser.store.db.setup import setup_database
from yt_diffuser.main.process_manager import start_loop
from yt_diffuser.main.watchdog import watchdog_process

def main(config: AppConfig, debug=False):
    """ メイン関数
    """
    logger.debug("Start yt_diffuser")

    setup_database(
        db_file=config.DB_FILE,
        db_update_file=config.DB_UPDATE_FILE,
        db_version=config.DB_VERSION
    )

    if debug:
        watchdog_process(procedure=start_loop, args=(config,))
    else:
        start_loop(config)

if __name__ == '__main__':
    main(AppConfig(), os.environ.get('DEBUG') == '1')
