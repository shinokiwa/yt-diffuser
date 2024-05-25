"""
yt_diffuser.utils.event.types.generate_status のテスト
"""
import pytest
from pytest_mock import MockerFixture

from yt_diffuser.utils.event.types.generate_status import *

class TestGenerateStatusEvent:

    def test_send_process_spec(self, mocker:MockerFixture):
        """
        send_process

        it:
            - 別プロセスにイベントを送信する。
        """
        q = multiprocessing.Queue()

        GenerateStatusEvent.send_process(q, GenerateStatusEvent.Status.READY,
            base_model_label="base",
            lora_model_label="lora",
            controlnet_model_label="controlnet",
            error="error"
        )
        assert q.get() == ("generator", True, {
            'status': 'ready',
            'base_model_label': 'base',
            'lora_model_label': 'lora',
            'controlnet_model_label': 'controlnet',
            'error': 'error'
        })