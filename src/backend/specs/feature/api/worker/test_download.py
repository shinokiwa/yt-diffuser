""" /api/worker/download の機能テスト
"""
import pytest
import requests
import json
import threading

from huggingface_hub.file_download import repo_folder_name

from specs.feature.testutils.app import setup_app
from yt_diffuser.config import AppConfig
from yt_diffuser.store import connect_database, HFModelStore

@pytest.mark.describe('API /api/worker/download の機能テスト')
@pytest.mark.it('ダウンロード処理を開始する。')
@pytest.mark.it('ダウンロード中はSSEで進捗を通知する。')
def test_download(setup_app:AppConfig):

    repo_id = 'CompVis/stable-diffusion-v1-4'
    revision = 'fp16'

    messages = []
    def _message():
        """ メッセージを受け取る
        """
        message = requests.get('http://localhost:8000/api/sse/message', stream=True)
        assert message.status_code == 200
        for _line in message.iter_lines():
            line = _line.decode('utf-8')
            if line == '' or line == 'data: ':
                continue
            messages.append(line)
            if line.startswith('data: download-complete:'):
                break
        message.close()
        print ('_message closed')

    def _download ():
        """ ダウンロードをリクエスト
        """
        res = requests.post('http://localhost:8000/api/worker/download')
        assert res.status_code == 200
        assert res.json() == {'status': 'ok'}
        print ('_download closed')

    progresses = []
    def _progress ():
        """ ダウンロード進捗状況を受け取る
        """

        downlaod = requests.get('http://localhost:8000/api/sse/download', stream=True)
        assert downlaod.status_code == 200

        for _line in downlaod.iter_lines():
            line = _line.decode('utf-8')
            if line == '' or line == 'data: {}':
                continue
            data = json.loads(line[len('data: '):])

            progresses.append(data)
            if data['progress'] >= 10:
                break
        downlaod.close()
        print ('_progress closed')

    p1 = threading.Thread(target=_message)
    p2 = threading.Thread(target=_download)
    p3 = threading.Thread(target=_progress)
    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()

    assert messages[0] == f"data: download-start:{repo_id}:{revision}"
    assert messages[1] == f"data: download-complete:{repo_id}:{revision}"

    assert progresses[0]['target'] == f"{repo_id}:{revision}"
    assert progresses[0]['total'] == 10
    assert progresses[0]['progress'] == 0
    assert progresses[0]['percentage'] == 0.0

    assert progresses[-1]['percentage'] >= 100.0
    
    model = HFModelStore(setup_app, repo_id=repo_id, revision=revision)
    assert model.exists()
    conn = connect_database(setup_app.DB_FILE)
    r = conn.execute("SELECT * FROM models WHERE path_name = ? AND revision = ?", (str(model.path), model.revision))
    row = r.fetchone()

    r = conn.execute("SELECT * FROM models")
    assert r.fetchall() == [(1, str(model.path), model.name, model.revision, model.class_name)]
    assert row['path_name'] == model.path
