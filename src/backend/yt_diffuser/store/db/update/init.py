""" DBの初期化を行う
"""
import sqlite3
from sqlite3 import OperationalError

from logging import getLogger; logger = getLogger(__name__)

from yt_diffuser.store.db.op.database_status import create_table as database_status_create_table, set as database_status_set, VERSION_KEY
from yt_diffuser.store.db.op.models import create_table as create_table_models
from yt_diffuser.store.db.op.models_hf_refs import create_table as create_table_models_hf_refs
from yt_diffuser.store.db.op.models_hf_snapshots import create_table as create_table_models_hf_snapshots

def init_database (conn:sqlite3.Connection, db_version:int):
    """ DBの初期化を行う
    """

    try: 
        database_status_create_table(conn)

        create_table_models(conn)
        create_table_models_hf_refs(conn)
        create_table_models_hf_snapshots(conn)

        database_status_set(conn, VERSION_KEY, db_version)

        conn.commit()
    except OperationalError as e:
        conn.rollback()
        logger.error(e)
        raise e
    