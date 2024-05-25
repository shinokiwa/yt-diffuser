"""
yt_diffuser.utils.event.types.file_system のテスト
"""
import pytest
from pytest_mock import MockerFixture

import multiprocessing

from yt_diffuser.utils.event.types.file_system import *


class TestFilesystemEvent:

    def test_send_spec(self, mocker:MockerFixture):
        """
        send

        it:
            - イベントを送信する。
        """
        mock_send_event = mocker.patch("yt_diffuser.utils.event.types.base_event.send_event")

        FilesystemEvent.send(FilesystemEvent.Type.EXIST, "test/path")
        assert mock_send_event.call_args.args[0] == "filesystem"
        assert mock_send_event.call_args.args[1] == False
        assert mock_send_event.call_args.args[2] == {"type": "exist", "target": "test/path"}
    
    def test_send_process_spec(self, mocker:MockerFixture):
        """
        send_process

        it:
            - 別プロセスにイベントを送信する。
        """
        q = multiprocessing.Queue()

        FilesystemEvent.send_process(q, FilesystemEvent.Type.EXIST, "test/path")
        assert q.get(timeout=5.0) == ("filesystem", False, {"type": "exist", "target": "test/path"})
