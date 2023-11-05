""" web_sender.py のテスト
"""
import pytest
import multiprocessing

from yt_diffuser.worker.web_sender import set_send_queue, get_send_queue

@pytest.mark.describe('set_send_queue, get_send_queue')
@pytest.mark.it('キューを設定し、取得する')
def test_set_send_queue_and_get_send_queue_spec():
    q = multiprocessing.Queue()
    set_send_queue(q)
    assert get_send_queue() == q

