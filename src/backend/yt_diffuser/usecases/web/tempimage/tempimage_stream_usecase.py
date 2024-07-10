import logging; logger = logging.getLogger(__name__)
from pathlib import Path

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent
from injector import inject

from yt_diffuser.types.web.event import WebEvent, WebEventType
from ..event.event_usecase import EventUseCase
from yt_diffuser.types.path import AppPath

class ImageWatchHandler(FileSystemEventHandler):
    """
    画像ファイルの変更をハンドリングするクラス
    """
    @inject
    def __init__(self, usecase: EventUseCase):
        super().__init__()
        self.usecase = usecase
    
    def trigger(self, event:FileSystemEvent):
        """
        イベントリスナーにイベントを配信する。

        args:
            event (FileSystemEvent): イベントデータ
        """
        if event.is_directory:
            return

        filename = Path(event.src_path).name
        web_event = WebEvent(
            type=WebEventType.TEMPFILE,
            args={
                "event_type": event.event_type,
                "filename": filename
            }
        )
        self.usecase.trigger(web_event.model_dump())
    
    def on_created(self, event:FileSystemEvent):
        self.trigger(event)
    
    def on_modified(self, event:FileSystemEvent):
        self.trigger(event)
    
    def on_deleted(self, event:FileSystemEvent):
        self.trigger(event)

    #def on_any_event(self, event:FileSystemEvent):
    #    self.trigger(event)


class TempImageStreamUseCase:
    """
    画像ファイルの変更を監視するクラス
    """

    @inject
    def __init__(self, app_path: AppPath, handler: ImageWatchHandler):
        self.observer = Observer()
        self.path = app_path
        self.handler = handler

    def run(self):
        directory = self.path.OUTPUT_TEMP_DIR
        self.observer.schedule(self.handler, directory, recursive=True)
        self.observer.start()
        self.observer.join()
