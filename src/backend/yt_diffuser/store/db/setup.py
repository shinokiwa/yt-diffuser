""" DBのセットアップを行う
"""
from logging import getLogger; logger = getLogger(__name__)
from pathlib import Path

from yt_diffuser.store.db import connect_database
from yt_diffuser.store.db.op.utils import is_exists_table
from yt_diffuser.store.db.op.database_status import (
    VERSION_KEY,
    get as database_status_get,
)
from yt_diffuser.store.db.update.update import update_database
from yt_diffuser.store.db.update.init import init_database

def setup_database (db_file: Path, db_update_file: Path, db_version: int):
    """DBのセットアップを行う。
    DBが存在しない場合は初期化し、存在する場合はアップデートの必要性を確認し、必要ならアップデートを行う。
    アップデート時は新規のDBを作成し、旧DBから必要なデータをコピー後、リネームしてオリジナルと差し替える。
    """
    logger.debug("Setup database.")

    # DBが存在しない場合は初期化のみ行う。
    if not db_file.exists():
        db_file.parent.mkdir(parents=True, exist_ok=True)

        conn = connect_database(db_file)
        init_database(conn, db_version)
        return
    
    originaldb = connect_database(db_file)

    is_need_update = False

    # database_statusテーブルが存在しない場合、
    # またはdatabase_statusテーブルに保存されているバージョン値が最新バージョンより古い場合はアップデートが必要
    if not is_exists_table(originaldb, 'database_status'):
        is_need_update = True
    else:
        current_version = database_status_get(originaldb, VERSION_KEY)
        if current_version is None or int(current_version) < db_version:
            is_need_update = True

    if is_need_update:
        # すでに新規DBが存在する場合は削除する
        if db_update_file.exists():
            db_update_file.unlink()

        newdb = connect_database(db_update_file)
        init_database(newdb, db_version)

        update_database(newdb, originaldb)

        originaldb.close()
        newdb.close()

        db_file.unlink()
        db_update_file.rename(db_file)

