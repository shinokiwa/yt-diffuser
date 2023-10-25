""" watchdog.pyのテスト """
from watchdog.events import FileModifiedEvent
from unittest.mock import MagicMock, patch
from yt_diffuser.main.watchdog import WatchdogDebugHandler, watchdog_process

class TestWatchdogDebugHandler:
    """describe: WatchdogDebugHandler ファイル変更を監視し、変更があった場合にアプリケーションを再起動する"""

    def test_on_modified(self, monkeypatch):
        """it: ファイル変更があった場合にメインプロセスを再起動する"""

        main_mock = MagicMock()
        web_main_mock = MagicMock()
        processing_main_mock = MagicMock()
        
        handler = WatchdogDebugHandler(main_mock, web_main_mock, processing_main_mock)
        
        with patch('multiprocessing.Process') as process_mock:
            handler.on_modified(FileModifiedEvent('test'))
            process_mock.assert_called_once_with(target=main_mock, args=(web_main_mock, processing_main_mock))

class TestWatchdogProcess:
    """describe: watchdog_process 開発用 ファイル変更監視と再起動のためのモジュール"""

    def test_watchdog_process(self, monkeypatch):
        """it: ファイル変更を監視し、変更があった場合にアプリケーションを再起動する"""
    
        main_mock = MagicMock()
        web_main_mock = MagicMock()
        processing_main_mock = MagicMock()
        
        with patch('yt_diffuser.main.watchdog.PollingObserver') as observer_mock, \
            patch('multiprocessing.Process') as process_mock:
            
            watchdog_process(main_mock, web_main_mock, processing_main_mock)
            
            observer_mock.return_value.schedule.assert_called_once()
            observer_mock.return_value.start.assert_called_once()
            observer_mock.return_value.join.assert_called_once()

