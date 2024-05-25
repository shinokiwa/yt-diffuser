"""
watchdog.pyのテスト
"""
import pytest

from watchdog.events import FileModifiedEvent

from yt_diffuser.dev_watcher import WatchdogDebugHandler, watchdog_process


class TestWatchdogDebugHandler:
    """describe: WatchdogDebugHandler ファイル変更監視"""

    def test_on_modified(self, monkeypatch):
        """it: on_modified ファイル変更があった場合にメインプロセスを再起動する"""

        procedure = MagicMock()
        handler = WatchdogDebugHandler(procedure, ('arg1', 'arg2'))
        
        with patch('multiprocessing.Process') as process_mock:
            handler.on_modified(FileModifiedEvent('test'))
            process_mock.assert_called_once_with(target=procedure, args=('arg1', 'arg2'))

class TestWatchdogProcess:
    """describe: watchdog_process 開発用 ファイル変更監視と再起動のためのモジュール"""

    def test_watchdog_process(self, monkeypatch):
        """it: ファイル変更を監視し、変更があった場合にアプリケーションを再起動する"""
    
        procedure = MagicMock()
        
        with patch('yt_diffuser.dev_watcher.PollingObserver') as observer_mock, \
            patch('multiprocessing.Process') as process_mock:
            
            watchdog_process(procedure, ('arg1', 'arg2'))
            
            observer_mock.return_value.schedule.assert_called_once()
            observer_mock.return_value.start.assert_called_once()
            observer_mock.return_value.join.assert_called_once()

