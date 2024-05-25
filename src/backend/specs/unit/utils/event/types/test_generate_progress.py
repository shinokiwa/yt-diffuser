"""
yt_diffuser.utils.event.types.generate_progress のテスト
"""
import pytest
from pytest_mock import MockerFixture

from yt_diffuser.utils.event.types.generate_progress import *

class TestGenerateStatusEvent:

    def test_send_process_spec(self, mocker:MockerFixture):
        """
        send_process

        it:
            - 別プロセスにイベントを送信する。
        """
        q = multiprocessing.Queue()

        GenerateProgressEvent.send_process(q,
            generate_total=10,
            generate_count=1,
            steps_total=100,
            steps_count=10,
            percentage=10.0,
            elapsed=10.0,
            remaining=10.0
        )
        assert q.get() == ("generate_progress", True, {
            "generate_total": 10,
            "generate_count": 1,
            "steps_total": 100,
            "steps_count": 10,
            "percentage": 10.0,
            "elapsed": 10.0,
            "remaining": 10.0
        })