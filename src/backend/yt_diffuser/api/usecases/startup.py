"""スタートアップ処理のユースケース
"""
from injector import Injector

from yt_diffuser.database.connection import Database, create_table

def startup():
    """
    スタートアップ処理
    """
    with Injector().get(Database) as db:
        create_table(db)