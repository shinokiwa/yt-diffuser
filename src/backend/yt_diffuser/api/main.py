import logging; logger = logging.getLogger('yt_diffuser')

import uvicorn

def main() -> None:
    """
    メイン関数

    Args:
        config (AppConfig): アプリケーション設定
    """
    logger.debug("Start yt_diffuser")

    uvicorn.run("yt_diffuser.api.web.app:create_app", host="0.0.0.0", port=8000, log_level="info", reload=True)
