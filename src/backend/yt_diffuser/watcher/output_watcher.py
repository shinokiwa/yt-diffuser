"""
outputディレクトリを監視し、ファイルの変更を通知するモジュール
"""
import logging; logger = logging.getLogger(__name__)
from multiprocessing import Queue

from watchdog.observers.polling import PollingObserver
from watchdog.events import FileSystemEventHandler

from yt_diffuser.config import AppConfig
from yt_diffuser.utils.message_queue import send_filesystem

class FileEventHandler(FileSystemEventHandler):

    def __init__(self, queue:Queue):
        super().__init__()
        self.message_queue = queue

    def on_created(self, event):
        if event.is_directory:
            return
        logger.debug(f"File created: {event.src_path}")
        send_filesystem(self.message_queue, 'created', event.src_path)

    def on_modified(self, event):
        if event.is_directory:
            return
        logger.debug(f"File modified: {event.src_path}")
        send_filesystem(self.message_queue, 'modified', event.src_path)
    
    def on_deleted(self, event):
        if event.is_directory:
            return
        logger.debug(f"File deleted: {event.src_path}")
        send_filesystem(self.message_queue, 'deleted', event.src_path)


def start_watchdog(config:AppConfig, queue:Queue):
    event_handler = FileEventHandler(queue=queue)
    observer = PollingObserver(timeout=5)
    observer.schedule(event_handler, path=config.OUTPUT_DIR, recursive=True)
    observer.start()
    logger.info(f"Start watchdog for {config.OUTPUT_DIR}")