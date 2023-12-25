"""
開発用 ファイル変更監視と再起動のためのモジュール
"""
import logging; logger = logging.getLogger(__name__)
from typing import Callable
import multiprocessing

from watchdog.observers.polling import PollingObserver
from watchdog.events import FileSystemEventHandler

# watchdogのログは抑制
logging.getLogger('watchdog').setLevel(logging.INFO)

class WatchdogDebugHandler(FileSystemEventHandler):
    """ ファイル変更を監視し、変更があった場合にアプリケーションを再起動する
    """
    def __init__(self, procedure:Callable, args:tuple=()):
        super().__init__()
        self.procedure = procedure
        self.args = args
        self.process = None
        self.context = multiprocessing.get_context('spawn')

    def on_modified(self, event):
        if event.is_directory:
            return
        logger.debug(f"File modified: {event.src_path}")
        self.start()
    
    def start (self):
        if self.process is not None:
            logger.debug("Terminate yt_diffuser")
            self.process.terminate()
            self.process.join()
            self.process = None

        logger.debug("Start yt_diffuser with watchdog")
        self.process = self.context.Process(target=self.procedure, args=self.args)
        self.process.start()

def watchdog_process(procedure:Callable, args:tuple=()):
    observer = PollingObserver(timeout=5)
    handler = WatchdogDebugHandler(procedure, args)
    handler.start()

    observer.schedule(handler, path='./yt_diffuser', recursive=True)
    observer.start()

    try:
        observer.join()
    except KeyboardInterrupt:
        observer.stop()
        observer.join()

