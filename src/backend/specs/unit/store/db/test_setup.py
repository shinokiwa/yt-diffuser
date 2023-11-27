""" setup.py のテスト
"""
import pytest
import tempfile
from unittest.mock import patch
from pathlib import Path
import sqlite3

from yt_diffuser.store.db.setup import setup_database

@pytest.mark.describe('setup_database')
@pytest.mark.it('データベースをセットアップする。')
@pytest.mark.it('データベースが存在しない場合は作成し、初期化する。')
def test_setup_database ():

    with tempfile.TemporaryDirectory() as tmpdir:
        with patch('yt_diffuser.store.db.setup.DB_FILE', Path(tmpdir) / "test.db") as DB_FILE, \
            patch('yt_diffuser.store.db.setup.init_database') as mock_init_database, \
            patch('yt_diffuser.store.db.setup.update_database') as mock_update_database:

            setup_database()
            
            assert DB_FILE.exists()

            assert mock_init_database.call_count == 1
            assert mock_update_database.call_count == 0

@pytest.mark.it('database_statusテーブルが存在しない場合はアップデートされる。')
def test_setup_database_nothing_status ():

    with tempfile.TemporaryDirectory() as tmpdir:
        with patch('yt_diffuser.store.db.setup.DB_FILE', Path(tmpdir) / "test.db") as DB_FILE, \
            patch('yt_diffuser.store.db.setup.DB_UPDATE_FILE', Path(tmpdir) / "test_update.db") as DB_UPDATE_FILE, \
            patch('yt_diffuser.store.db.setup.init_database') as mock_init_database, \
            patch('yt_diffuser.store.db.setup.update_database') as mock_update_database:

            DB_FILE.parent.mkdir(parents=True, exist_ok=True)
            sqlite3.connect(DB_FILE)

            setup_database()

            assert mock_init_database.call_count == 1
            assert mock_update_database.call_count == 1

@pytest.mark.it('database_statusテーブルのバージョンキーがない場合はアップデートされる。')
def test_setup_database_nothing_version_key ():

    with tempfile.TemporaryDirectory() as tmpdir:
        with patch('yt_diffuser.store.db.setup.DB_FILE', Path(tmpdir) / "test.db") as DB_FILE, \
            patch('yt_diffuser.store.db.setup.DB_UPDATE_FILE', Path(tmpdir) / "test_update.db") as DB_UPDATE_FILE, \
            patch('yt_diffuser.store.db.setup.init_database') as mock_init_database, \
            patch('yt_diffuser.store.db.setup.update_database') as mock_update_database:

            DB_FILE.parent.mkdir(parents=True, exist_ok=True)
            conn = sqlite3.connect(DB_FILE)
            conn.execute("CREATE TABLE database_status (key TEXT, value TEXT)")
            conn.commit()

            setup_database()

            assert mock_update_database.call_count == 1
            assert mock_init_database.call_count == 1

@pytest.mark.it('database_statusテーブルのバージョン情報が古い場合はアップデートされる。')
def test_setup_database_old_version ():

    with tempfile.TemporaryDirectory() as tmpdir:
        with patch('yt_diffuser.store.db.setup.DB_FILE', Path(tmpdir) / "test.db") as DB_FILE, \
            patch('yt_diffuser.store.db.setup.DB_UPDATE_FILE', Path(tmpdir) / "test_update.db") as DB_UPDATE_FILE, \
            patch('yt_diffuser.store.db.setup.init_database') as mock_init_database, \
            patch('yt_diffuser.store.db.setup.update_database') as mock_update_database:

            DB_FILE.parent.mkdir(parents=True, exist_ok=True)
            conn = sqlite3.connect(DB_FILE)

            conn.execute("CREATE TABLE database_status (key TEXT, value TEXT)")
            conn.execute("INSERT INTO database_status VALUES ('version', '0')")
            conn.commit()

            setup_database()

            assert mock_init_database.call_count == 1
            assert mock_update_database.call_count == 1

@pytest.mark.it('アップデートの際は新規DBを作成し、旧DBから必要なデータをコピー後、リネームしてオリジナルと差し替える。新規DBが存在する場合は削除して新たに作成する。')
def test_setup_database_udpate ():

    with tempfile.TemporaryDirectory() as tmpdir:
        with patch('yt_diffuser.store.db.setup.DB_FILE', Path(tmpdir) / "test.db") as DB_FILE, \
            patch('yt_diffuser.store.db.setup.DB_UPDATE_FILE', Path(tmpdir) / "test_update.db") as DB_UPDATE_FILE, \
            patch('yt_diffuser.store.db.setup.init_database') as mock_init_database, \
            patch('yt_diffuser.store.db.setup.update_database') as mock_update_database:

            DB_FILE.parent.mkdir(parents=True, exist_ok=True)
            sqlite3.connect(DB_FILE)

            conn = sqlite3.connect(DB_UPDATE_FILE)
            conn.execute("CREATE TABLE database_status (key TEXT, value TEXT)")
            conn.execute("INSERT INTO database_status VALUES ('version', '9999')")
            conn.commit()

            setup_database()

            assert mock_init_database.call_count == 1
            assert mock_update_database.call_count == 1

            assert not DB_UPDATE_FILE.exists()
            assert DB_FILE.exists()
