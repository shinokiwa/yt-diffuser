"""DBセットアップの実処理モジュール
"""
import sqlite3

def update_database (newdb: sqlite3.Connection, olddb: sqlite3.Connection):
    """ DBのアップデートを行う。
    newdbにolddbから必要なデータをコピーする。
    """

    # 今は関数を用意してあるだけ
    pass