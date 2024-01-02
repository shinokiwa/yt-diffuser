""" DBの初期化を行う
"""
import sqlite3
from sqlite3 import OperationalError
from importlib import import_module

from logging import getLogger; logger = getLogger(__name__)

from yt_diffuser.store.db.op.database_status import set as database_status_set, VERSION_KEY

def init_database (conn:sqlite3.Connection, db_version:int):
    """ DBの初期化を行う
    """

    try: 
        import_module('yt_diffuser.store.db.op.database_status').create_table(conn)
        import_module('yt_diffuser.store.db.op.model_info').create_table(conn)
        import_module('yt_diffuser.store.db.op.form_data').create_table(conn)
        import_module('yt_diffuser.store.db.op.prompt_archive').create_table(conn)

        database_status_set(conn, VERSION_KEY, db_version)

        conn.commit()
    except OperationalError as e:
        conn.rollback()
        logger.error(e)
        raise e
    