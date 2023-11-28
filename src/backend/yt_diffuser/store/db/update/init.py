""" DBの初期化を行う
"""
import sqlite3
from sqlite3 import OperationalError

from logging import getLogger; logger = getLogger(__name__)

from yt_diffuser.store.db.op.database_status import create_table as database_status_create_table, set as database_status_set, VERSION_KEY
from yt_diffuser.store.db.op.models import create_table as models_create_table

def init_database (conn:sqlite3.Connection, db_version:int):
    """ DBの初期化を行う
    """

    try: 
        database_status_create_table(conn)
        models_create_table(conn)

        database_status_set(conn, VERSION_KEY, db_version)

        conn.commit()
    except OperationalError as e:
        conn.rollback()
        logger.error(e)
        raise e
    