""" yt_diffuser.web.worker.download のテスト
"""
import pytest

from flask import Flask

from yt_diffuser.config import AppConfig
from yt_diffuser.web.api.download import bp

@pytest.fixture
def app ():
    app = Flask(__name__)
    app.config['APP_CONFIG'] = AppConfig()
    app.register_blueprint(bp)
    return app

class TestApiDownload:
    """
    /api/download のテスト
    """

    def test_start_spec (self, app, mocker):
        """
        /api/download/start

        it:
            ダウンロードを実行する。
        """
        mock_is_running = mocker.patch('yt_diffuser.web.api.download.is_running')
        mock_is_running.return_value = False
        mock_download = mocker.patch('yt_diffuser.web.api.download.download')

        client = app.test_client()
        response = client.post('/api/download/start', json={
            'repo_id': 'test_repo',
            'revision': 'test_revision'
        })
        assert response.status_code == 200
        assert response.json == {'status': 'ok'}
        assert mock_download.call_count == 1
        assert mock_download.call_args.kwargs == {
            'config': app.config['APP_CONFIG'],
            'repo_id': 'test_repo',
            'revision': 'test_revision'
        }

    def test_start_invalid (self, app, mocker):
        """
        /api/download/start エラー系

        it:
            リクエストボディはJSON形式で、以下のフィールドを含む。
            - repo_id: リポジトリID
            - revision: リビジョン
            既にダウンロードが実行中の場合は400エラーを返す。
        """
        mock_is_running = mocker.patch('yt_diffuser.web.api.download.is_running')
        mock_is_running.return_value = False

        client = app.test_client()

        # リクエストボディがJSON形式でない場合
        response = client.post('/api/download/start')
        assert response.status_code == 400
        assert response.json == {'status': 'ng', 'message': 'invalid-json'}

        # リクエストボディがJSON形式だが、必須フィールドがない場合
        response = client.post('/api/download/start', json={})
        assert response.status_code == 400
        assert response.json == {'status': 'ng', 'message': 'invalid-request', 'detail': [
            {'loc': ['repo_id'], 'msg': 'field required', 'type': 'value_error.missing'},
            {'loc': ['revision'], 'msg': 'field required', 'type': 'value_error.missing'}
        ]}

        # リクエストボディがJSON形式だが、フィールドの型が不正な場合
        # 双方ともstr型で入力内容に縛りがないため、エラーにならないのでテストなし。

        # ダウンロードが実行中の場合
        mock_is_running.return_value = True
        response = client.post('/api/download/start', json={
            'repo_id': 'test_repo',
            'revision': 'test_revision'
        })
        assert response.status_code == 400
        assert response.json == {'status': 'ng', 'message': 'download-running'}

    def test_stop_spec (self, app, mocker):
        """
        /api/download/stop

        it:
            処理中断
        """
        mock_terminate = mocker.patch('yt_diffuser.web.api.download.terminate')

        client = app.test_client()
        response = client.get('/api/download/stop')
        assert response.status_code == 200
        assert response.json == {'status': 'ok'}
        assert mock_terminate.call_count == 1
