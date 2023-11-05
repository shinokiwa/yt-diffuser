""" worker のテスト
"""
import pytest
from flask import Blueprint

from yt_diffuser.web.api.worker import worker_bp, download

@pytest.mark.describe('worker_bp')
@pytest.mark.it('worker_bpはBlueprintオブジェクト')
def test_worker_bp_spec():
    assert type(worker_bp) == Blueprint

@pytest.mark.describe('download')
@pytest.mark.it('ワーカープロセスに指示を出す。')
def test_download_spec(mocker):
    mock_get_send_queue = mocker.patch('yt_diffuser.web.api.worker.get_send_queue', return_value=mocker.Mock(put=mocker.Mock()))
    data = download()

    assert data == 'ok'
    assert mock_get_send_queue.call_count == 1
    assert mock_get_send_queue.return_value.put.call_count == 1
