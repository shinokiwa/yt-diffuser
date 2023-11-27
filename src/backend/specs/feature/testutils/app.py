""" テスト用ユーティリティ
"""
import pytest
import requests
import time

from yt_diffuser.store.db.setup import setup_database
from yt_diffuser.main.process_manager import start_processes

@pytest.fixture(scope='module')
def setup_app():
    """ テスト用のアプリケーションをセットアップする
    """
    setup_database()
    start_processes()
    # ポート8000でサーバーが立ち上がるまで待つ
    start_time = time.time()
    while True:
        try:
            res = requests.get('http://localhost:8000/api/health')
            if res.status_code == 200:
                break
        except:
            pass
        if time.time() - start_time > 10:
            raise Exception('timeout')
        time.sleep(0.1)