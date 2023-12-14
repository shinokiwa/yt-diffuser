"""
/api/worker/download の機能テスト
"""
import pytest
import json
import time
import threading
from pathlib import Path
from logging import getLogger; logger = getLogger(__name__)

from flask import Flask
from huggingface_hub.hf_api import (
    ModelInfo,
    RepoFile
)

from specs.feature.testutils.app import app

def dummy_hf_hub_download(*args, **kwargs):
    time.sleep(1)
    return str(Path(__file__).parent / "model_index.json")

def dummy_hf_api_repo_info(*args, **kwargs):
    res = ModelInfo()
    res.sha = "revision"
    res.siblings = [
        RepoFile(rfilename="scheduler/file1.txt"),
        RepoFile(rfilename="text_encoder/file2.txt"),
        RepoFile(rfilename="tokenizer/file3.txt"),
        RepoFile(rfilename="unet/file4.txt"),
    ]
    return res


class TestFeatureApiWorkerDownload:
    """
    /api/worker/download の機能テスト
    """

    def test_download(self, app:Flask, mocker):
        """
        ダウンロード処理を開始する。
        ダウンロード中はSSEで進捗を通知する。
        """
        mock_hf_hub_download = mocker.patch('yt_diffuser.download.main.hf_hub_download',
                                            side_effect=dummy_hf_hub_download
                                            )
        mock_repo_info = mocker.patch('yt_diffuser.download.main.HfApi.repo_info', 
                                        side_effect=dummy_hf_api_repo_info
                                        )
        client = app.test_client()

        repo_id = "test_repo_id"
        revision = "test_revision"

        messages = []
        message = client.get('/api/sse/message', headers={'Accept': 'text/event-stream'})
        assert message.status_code == 200
        logger.debug ("message connected")

        def recv_message():
            for _line in message.response:
                line = _line.decode('utf-8').strip()[len('data: '):]
                if line == '': continue
                logger.debug ("_message", line)
                data = json.loads(line)
                messages.append(data)
                if len(messages) >= 2: break
            message.close()

        sse1 = threading.Thread(target=recv_message, daemon=True)
        sse1.start()

        progresses = []
        progress = client.get('/api/sse/download', headers={'Accept': 'text/event-stream'})
        assert progress.status_code == 200
        logger.debug ("progress connected")

        def recv_progress ():
            for _line in progress.response:
                line = _line.decode('utf-8').strip()[len('data: '):]
                if line == '': continue
                data = json.loads(line)
                progresses.append(data)
                if data['progress'] >= 10: break
            progress.close()

        sse2 = threading.Thread(target=recv_progress, daemon=True)
        sse2.start()

        res = client.post('/api/download/start', json={
            'repo_id': repo_id,
            'revision': revision
        })
        assert res.status_code == 200
        assert res.json == {'status': 'ok'}
        logger.debug ("download started")

        sse1.join()
        sse2.join()

        assert messages[0] == f"data: download-start:{repo_id}:{revision}"
        assert messages[1] == f"data: download-complete:{repo_id}:{revision}"

        assert progresses[0]['target'] == f"{repo_id}:{revision}"
        assert progresses[0]['total'] == 10
        assert progresses[0]['progress'] == 0
        assert progresses[0]['percentage'] == 0.0

        assert progresses[-1]['percentage'] >= 100.0
        