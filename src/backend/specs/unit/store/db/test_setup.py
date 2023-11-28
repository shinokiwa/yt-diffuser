""" setup.py のテスト
"""
import pytest
import tempfile
from pathlib import Path
import sqlite3

from yt_diffuser.store.db.setup import setup_database

@pytest.mark.describe('setup_database')
@pytest.mark.it('データベースをセットアップする。')
@pytest.mark.it('データベースが存在しない場合は作成し、初期化する。')
def test_setup_database (mocker):

    with tempfile.TemporaryDirectory() as tmpdir:
        db_file = Path(tmpdir) / "test.db"
        db_update_file = Path(tmpdir) / "test_update.db"

        mock_init_database = mocker.patch('yt_diffuser.store.db.setup.init_database')
        mock_update_database = mocker.patch('yt_diffuser.store.db.setup.update_database')

        setup_database(db_file=db_file, db_update_file=db_update_file, db_version=1)
            
        assert db_file.exists()

        assert mock_init_database.call_count == 1
        assert mock_update_database.call_count == 0

@pytest.mark.it('database_statusテーブルが存在しない場合はアップデートされる。')
def test_setup_database_nothing_status (mocker):

    with tempfile.TemporaryDirectory() as tmpdir:
        db_file = Path(tmpdir) / "test.db"
        db_update_file = Path(tmpdir) / "test_update.db"

        mock_init_database = mocker.patch('yt_diffuser.store.db.setup.init_database')
        mock_update_database = mocker.patch('yt_diffuser.store.db.setup.update_database')

        db_file.parent.mkdir(parents=True, exist_ok=True)
        sqlite3.connect(db_file)

        setup_database(db_file=db_file, db_update_file=db_update_file, db_version=1)

        assert mock_init_database.call_count == 1
        assert mock_update_database.call_count == 1


@pytest.mark.it('database_statusテーブルのバージョンキーがない場合はアップデートされる。')
def test_setup_database_nothing_version_key (mocker):

    with tempfile.TemporaryDirectory() as tmpdir:
        db_file = Path(tmpdir) / "test.db"
        db_update_file = Path(tmpdir) / "test_update.db"

        mock_init_database = mocker.patch('yt_diffuser.store.db.setup.init_database')
        mock_update_database = mocker.patch('yt_diffuser.store.db.setup.update_database')

        db_file.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(db_file)
        conn.execute("CREATE TABLE database_status (key TEXT, value TEXT)")
        conn.commit()

        setup_database(db_file=db_file, db_update_file=db_update_file, db_version=1)

        assert mock_update_database.call_count == 1
        assert mock_init_database.call_count == 1


@pytest.mark.it('database_statusテーブルのバージョン情報が古い場合はアップデートされる。')
def test_setup_database_old_version (mocker):

    with tempfile.TemporaryDirectory() as tmpdir:
        db_file = Path(tmpdir) / "test.db"
        db_update_file = Path(tmpdir) / "test_update.db"

        mock_init_database = mocker.patch('yt_diffuser.store.db.setup.init_database')
        mock_update_database = mocker.patch('yt_diffuser.store.db.setup.update_database')        

        db_file.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(db_file)

        conn.execute("CREATE TABLE database_status (key TEXT, value TEXT)")
        conn.execute("INSERT INTO database_status VALUES ('version', '0')")
        conn.commit()

        setup_database(db_file=db_file, db_update_file=db_update_file, db_version=1)

        assert mock_init_database.call_count == 1
        assert mock_update_database.call_count == 1

@pytest.mark.it('アップデートの際は新規DBを作成し、旧DBから必要なデータをコピー後、リネームしてオリジナルと差し替える。新規DBが存在する場合は削除して新たに作成する。')
def test_setup_database_udpate (mocker):

    with tempfile.TemporaryDirectory() as tmpdir:
        db_file = Path(tmpdir) / "test.db"
        db_update_file = Path(tmpdir) / "test_update.db"

        mock_init_database = mocker.patch('yt_diffuser.store.db.setup.init_database')
        mock_update_database = mocker.patch('yt_diffuser.store.db.setup.update_database')        

        db_file.parent.mkdir(parents=True, exist_ok=True)
        sqlite3.connect(db_file)

        conn = sqlite3.connect(db_update_file)
        conn.execute("CREATE TABLE database_status (key TEXT, value TEXT)")
        conn.execute("INSERT INTO database_status VALUES ('version', '9999')")
        conn.commit()

        setup_database(db_file=db_file, db_update_file=db_update_file, db_version=1)

        assert mock_init_database.call_count == 1
        assert mock_update_database.call_count == 1

        assert not db_update_file.exists()
        assert db_file.exists()


@pytest.mark.it('database_statusテーブルのバージョン情報が同じか新しい場合はアップデートされない。')
def test_setup_database_old_version (mocker):

    with tempfile.TemporaryDirectory() as tmpdir:
        db_file = Path(tmpdir) / "test.db"
        db_update_file = Path(tmpdir) / "test_update.db"

        mock_init_database = mocker.patch('yt_diffuser.store.db.setup.init_database')
        mock_update_database = mocker.patch('yt_diffuser.store.db.setup.update_database')        

        db_file.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(db_file)

        conn.execute("CREATE TABLE database_status (key TEXT, value TEXT)")
        conn.execute("INSERT INTO database_status VALUES ('version', '2')")
        conn.commit()

        setup_database(db_file=db_file, db_update_file=db_update_file, db_version=1)
        assert mock_init_database.call_count == 0
        assert mock_update_database.call_count == 0

        setup_database(db_file=db_file, db_update_file=db_update_file, db_version=2)
        assert mock_init_database.call_count == 0
        assert mock_update_database.call_count == 0