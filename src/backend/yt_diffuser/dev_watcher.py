"""
開発用 ファイル変更監視と再起動のためのモジュール
"""
import logging; logger = logging.getLogger(__name__)
import os
import sys
from pathlib import Path

from watchdog.observers.polling import PollingObserver
from watchdog.events import FileSystemEventHandler

from yt_diffuser.web.process.download import terminate as terminate_download
from yt_diffuser.web.process.generate_image import terminate as terminate_generate_image

# watchdogのログは抑制
logging.getLogger('watchdog').setLevel(logging.INFO)

class WatchdogDebugHandler(FileSystemEventHandler):
    """ ファイル変更を監視し、変更があった場合にアプリケーションを再起動する
    """
    def on_modified(self, event):
        if event.is_directory:
            return
        logger.debug(f"File modified: {event.src_path}")
        logger.debug("Terminate download process")
        terminate_download()
        logger.debug("Terminate generate_image process")
        terminate_generate_image()
        logger.debug("Restart yt_diffuser")
        os.chdir(Path(__file__).parents[1])
        os.execl(sys.executable, sys.executable, *['-m', 'yt_diffuser'] + sys.argv[1:])

def watchdog_process():
    observer = PollingObserver(timeout=5)
    handler = WatchdogDebugHandler()

    observer.schedule(handler, path='./yt_diffuser', recursive=True)
    observer.start()

    logger.debug("Watchdog debugger process started")
