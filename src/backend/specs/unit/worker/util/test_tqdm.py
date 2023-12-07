""" tqdm.py のテスト
"""
import pytest
import multiprocessing

from yt_diffuser.worker.util.tqdm import WorkerProgress

@pytest.mark.describe("WorkerProgress")
@pytest.mark.it("進捗を送信キューに入れる。")
def test_worker_progress_display_spec():

    q = multiprocessing.Queue()
    progress = WorkerProgress(total=100, delay=0, mininterval=0, queue=q)

    event, data = q.get()
    assert event == 'progress'
    assert data.keys() == {'total', 'progress', 'percentage', 'elapsed', 'remaining'}
    assert data['total'] == 100
    assert data['progress'] == 0
    assert data['percentage'] == 0.0
    assert data['elapsed'] == 0.0
    assert data['remaining'] == -1

    progress.update(10)
    event, data = q.get()

    assert event == 'progress'
    assert data.keys() == {'total', 'progress', 'percentage', 'elapsed', 'remaining'}
    assert data['total'] == 100
    assert data['progress'] == 10
    assert data['percentage'] == 10.0
    assert data['elapsed'] > 0
    assert data['remaining'] >= 0


@pytest.mark.it("トータルがゼロの時は即完了。")
def test_worker_progress_display_total_zero():

    q = multiprocessing.Queue()
    progress = WorkerProgress(total=0, delay=0, mininterval=0, queue=q)

    event, data = q.get()

    assert event == 'progress'
    assert data.keys() == {'total', 'progress', 'percentage', 'elapsed', 'remaining'}
    assert data['total'] == 0
    assert data['progress'] == 0
    assert data['percentage'] == 0.0
    assert data['elapsed'] == 0.0
    assert data['remaining'] == -1

    