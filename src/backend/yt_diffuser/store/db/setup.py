""" DBのセットアップを行う
"""
from logging import getLogger; logger = getLogger(__name__)
import sqlite3
from yt_diffuser.constant import (
    DB_FILE,
    DB_UPDATE_FILE,
    DB_VERSION
)

from yt_diffuser.store.db.op.utils import is_exists_table
from yt_diffuser.store.db.op.database_status import (
    VERSION_KEY,
    get as database_status_get,
)
from yt_diffuser.store.db.update.update import update_database
from yt_diffuser.store.db.update.init import init_database

def setup_database ():
    """DBのセットアップを行う。
    DBが存在しない場合は初期化し、存在する場合はアップデートの必要性を確認し、必要ならアップデートを行う。
    アップデート時は新規のDBを作成し、旧DBから必要なデータをコピー後、リネームしてオリジナルと差し替える。
    """

    DB_FILE.parent.mkdir(parents=True, exist_ok=True)

    # DBが存在しない場合は初期化のみ行う。
    if not DB_FILE.exists():
        conn = sqlite3.connect(DB_FILE)
        init_database(conn)
        return
    
    originaldb = sqlite3.connect(DB_FILE)

    is_need_update = False

    # database_statusテーブルが存在しない場合、
    # またはdatabase_statusテーブルに保存されているバージョン値が最新バージョンより古い場合はアップデートが必要
    if not is_exists_table(originaldb, 'database_status'):
        is_need_update = True
    else:
        current_version = database_status_get(originaldb, VERSION_KEY)
        if current_version is None or int(current_version) < DB_VERSION:
            is_need_update = True

    if is_need_update:
        # すでに新規DBが存在する場合は削除する
        if DB_UPDATE_FILE.exists():
            DB_UPDATE_FILE.unlink()

        newdb = sqlite3.connect(DB_UPDATE_FILE)
        init_database(newdb)

        update_database(newdb, originaldb)

        originaldb.close()
        newdb.close()

        DB_FILE.unlink()
        DB_UPDATE_FILE.rename(DB_FILE)

