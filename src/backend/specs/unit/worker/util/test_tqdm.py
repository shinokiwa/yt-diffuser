""" tqdm.py のテスト
"""
import pytest
import time

from yt_diffuser.worker.util.tqdm import WorkerProgress, DownloadProgress

@pytest.fixture(scope='function')
def mock_web_sender(mocker):
    return mocker.MagicMock(put=mocker.MagicMock())

@pytest.mark.describe("WorkerProgress")
@pytest.mark.it("進捗を送信キューに入れる。")
def test_worker_progress_display_spec(mocker, mock_web_sender):

    mocker.patch('yt_diffuser.worker.util.tqdm.get_send_queue', return_value=mock_web_sender)

    progress = WorkerProgress(total=100, delay=0, mininterval=0)

    assert mock_web_sender.put.call_count == 1
    assert mock_web_sender.put.call_args[0][0][0] == 'progress'
    assert mock_web_sender.put.call_args[0][0][1].keys() == {'cancelable', 'total', 'progress', 'percentage', 'elapsed', 'remaining'}
    assert mock_web_sender.put.call_args[0][0][1]['cancelable'] == True
    assert mock_web_sender.put.call_args[0][0][1]['total'] == 100
    assert mock_web_sender.put.call_args[0][0][1]['progress'] == 0
    assert mock_web_sender.put.call_args[0][0][1]['percentage'] == 0.0
    assert mock_web_sender.put.call_args[0][0][1]['elapsed'] == 0.0
    assert mock_web_sender.put.call_args[0][0][1]['remaining'] == -1

    progress.update(10)

    assert mock_web_sender.put.call_count == 2
    assert mock_web_sender.put.call_args[0][0][0] == 'progress'
    assert mock_web_sender.put.call_args[0][0][1].keys() == {'cancelable', 'total', 'progress', 'percentage', 'elapsed', 'remaining'}
    assert mock_web_sender.put.call_args[0][0][1]['cancelable'] == True
    assert mock_web_sender.put.call_args[0][0][1]['total'] == 100
    assert mock_web_sender.put.call_args[0][0][1]['progress'] == 10
    assert mock_web_sender.put.call_args[0][0][1]['percentage'] == 10.0
    assert mock_web_sender.put.call_args[0][0][1]['elapsed'] > 0
    assert mock_web_sender.put.call_args[0][0][1]['remaining'] >= 0


@pytest.mark.it("トータルがゼロの時は即完了。")
def test_worker_progress_display_total_zero(mocker, mock_web_sender):

    mocker.patch('yt_diffuser.worker.util.tqdm.get_send_queue', return_value=mock_web_sender)

    progress = WorkerProgress(total=0, delay=0, mininterval=0)

    assert mock_web_sender.put.call_count == 1
    assert mock_web_sender.put.call_args[0][0][0] == 'progress'
    assert mock_web_sender.put.call_args[0][0][1].keys() == {'cancelable', 'total', 'progress', 'percentage', 'elapsed', 'remaining'}
    assert mock_web_sender.put.call_args[0][0][1]['cancelable'] == True
    assert mock_web_sender.put.call_args[0][0][1]['total'] == 0
    assert mock_web_sender.put.call_args[0][0][1]['progress'] == 0
    assert mock_web_sender.put.call_args[0][0][1]['percentage'] == 0.0
    assert mock_web_sender.put.call_args[0][0][1]['elapsed'] == 0.0
    assert mock_web_sender.put.call_args[0][0][1]['remaining'] == -1

@pytest.mark.describe("DownloadProgress")
@pytest.mark.it("cancelableがFalseなだけで、WorkerProgressと同じ。")
def test_download_progress (mocker, mock_web_sender):

    mocker.patch('yt_diffuser.worker.util.tqdm.get_send_queue', return_value=mock_web_sender)

    progress = DownloadProgress(total=100, delay=0, mininterval=0)
    assert progress.cancelable == False

    progress.update(10)

    assert mock_web_sender.put.call_args[0][0][0] == 'progress'
    assert mock_web_sender.put.call_args[0][0][1].keys() == {'cancelable', 'total', 'progress', 'percentage', 'elapsed', 'remaining'}
    assert mock_web_sender.put.call_args[0][0][1]['cancelable'] == False
    