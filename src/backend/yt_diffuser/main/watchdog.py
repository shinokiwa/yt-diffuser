""" 開発用 ファイル変更監視と再起動のためのモジュール
"""
import logging; logger = logging.getLogger(__name__)
from typing import Callable
from watchdog.observers.polling import PollingObserver
from watchdog.events import FileSystemEventHandler
import multiprocessing

# watchdogのログは抑制
logging.getLogger('watchdog').setLevel(logging.INFO)

class WatchdogDebugHandler(FileSystemEventHandler):
    """ ファイル変更を監視し、変更があった場合にアプリケーションを再起動する
    """
    def __init__(self, main:Callable, web_main:Callable, processing_main:Callable):
        super().__init__()
        self.main = main
        self.args = (web_main, processing_main)
        self.process = None

    def on_modified(self, event):
        logger.debug(f"File modified: {event.src_path}")
        self.start()
    
    def start (self):
        if self.process is not None:
            logger.debug("Terminate yt_diffuser")
            self.process.terminate()
            self.process.join()

        logger.debug("Start yt_diffuser with watchdog")
        self.process = multiprocessing.Process(target=self.main, args=self.args)
        self.process.start()

def watchdog_process(main:Callable, web_main:Callable, processing_main:Callable):
    observer = PollingObserver()
    handler = WatchdogDebugHandler(main, web_main, processing_main)
    handler.start()

    observer.schedule(handler, path='./yt_diffuser', recursive=True)
    observer.start()

    try:
        observer.join()
    except KeyboardInterrupt:
        observer.stop()
        observer.join()

