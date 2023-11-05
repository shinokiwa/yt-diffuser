""" worker_sender.py のテスト
"""
import pytest
from unittest.mock import patch
import multiprocessing
from multiprocessing.queues import Queue

from yt_diffuser.web.worker_sender import set_send_queue, get_send_queue

@pytest.mark.describe('set_send_queue, get_send_queue')
@pytest.mark.it('キューを設定し、取得する')
def test_set_send_queue_and_get_send_queue_spec():
    q = multiprocessing.Queue()
    set_send_queue(q)
    assert get_send_queue() == q
