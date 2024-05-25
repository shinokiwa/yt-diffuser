"""
/api/worker/download の機能テスト
"""
import pytest
import json
import threading
from logging import getLogger; logger = getLogger(__name__)

from flask import Flask

from specs.utils.test_utils.app import app

class TestFeatureApiWorkerDownload:
    """
    /api/worker/download の機能テスト
    """

    def test_download(self, app:Flask, mocker):
        """
        ダウンロード処理を開始する。
        ダウンロード中はSSEで進捗を通知する。
        """
        client = app.test_client()

        repo_id = "test/repo_id"
        revision = "test_revision"

        messages = []
        message = client.get('/api/sse/message', headers={'Accept': 'text/event-stream'})
        assert message.status_code == 200
        logger.debug ("message connected")

        def recv_message():
            i = 0
            for _line in message.response:
                line = _line.decode('utf-8').strip()[len('data: '):]
                logger.debug (f"_message data: {line}")

                if line == '':
                    i += 1
                    if i > 2: break
                    continue
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
            i = 0
            for _line in progress.response:
                line = _line.decode('utf-8').strip()[len('data: '):]
                logger.debug (f"_progress data:{line}")

                if line == '':
                    i += 1
                    if i > 2: break
                    continue
                data = json.loads(line)
                progresses.append(data)
                if data['progress'] >= 5: break
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

        assert messages[0]['label'] == "download-start"
        assert messages[0]['target'] == f"{repo_id}:{revision}"
        assert messages[1]['label'] == "download-complete"
        assert messages[1]['target'] == f"{repo_id}:{revision}"

        assert progresses[0]['target'] == f"{repo_id}:{revision}"
        assert progresses[0]['total'] == 5
        assert progresses[0]['progress'] == 0
        assert progresses[0]['percentage'] == 0.0

        assert progresses[-1]['progress'] == 5
        assert progresses[-1]['percentage'] >= 100.0
