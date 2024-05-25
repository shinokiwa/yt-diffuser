import sys
import logging; logger = logging.getLogger('yt_diffuser')

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
        logging.basicConfig(stream=sys.stdout)
        logger.setLevel(level=logging.DEBUG)

    logger.debug("Start yt_diffuser")

    app = create_app(
        config=config
    )

    logger.debug("Start waitress")
    serve(app, host='0.0.0.0', port=8000, threads=100)