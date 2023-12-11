""" ゆとりでふーざー メインモジュール

Web APIプロセスのメイン処理
"""
from logging import getLogger; logger = getLogger(__name__)

import os

from waitress import serve

from yt_diffuser.config import AppConfig
from yt_diffuser.web.app import create_app

def main(config:AppConfig, debug:bool) -> None:
    """ メイン関数
    """
    if debug:
        import logging; logging.basicConfig(level=logging.DEBUG)

    logger.debug("Start yt_diffuser")

    app = create_app(config)

    app.debug = debug

    serve(app, host='0.0.0.0', port=8000)

if __name__ == '__main__':   # pragma: no cover
    main(
        config=AppConfig(),
        debug=os.environ.get('DEBUG') == '1'
    )