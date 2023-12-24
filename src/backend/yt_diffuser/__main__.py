""" ゆとりでふーざー メインモジュール

Web APIプロセスのメイン処理
"""
import sys
import os
import logging; logger = logging.getLogger('yt_diffuser')
logging.basicConfig(stream=sys.stdout)

from waitress import serve

from yt_diffuser.config import AppConfig
from yt_diffuser.web.app import create_app

def main(config:AppConfig) -> None:
    """
    メイン関数

    - Flask APPを作成し、waitressで起動する。
    - 環境変数DEBUGが1の場合はデバッグモードで起動する。

    Args:
        config (AppConfig): アプリケーション設定
    """
    if config.debug:
        logger.setLevel(level=logging.DEBUG)

    logger.debug("Start yt_diffuser")

    app = create_app(
        config=config
    )

    if config.debug:
        app.run(host='0.0.0.0', port=8000, debug=True)
    else:
        serve(app, host='0.0.0.0', port=8000)

if __name__ == '__main__':   # pragma: no cover
    main(
        config=AppConfig(
            debug=os.environ.get('DEBUG') == '1'
        )
    )