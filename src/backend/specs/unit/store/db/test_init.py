""" db/__init__.pyのテスト
"""
import pytest
import sqlite3
import datetime
from yt_diffuser.store import db

@pytest.mark.describe("connect_database")
@pytest.mark.it("データベースに接続する")
def test_connect_database():
    conn = db.connect_database(":memory:")
    assert isinstance(conn, sqlite3.Connection)
    conn.close()

@pytest.mark.describe("adapt_date")
@pytest.mark.it("datetime.date を timezone-naive ISO 8601 date に変換する")
def test_adapt_date():
    date = datetime.date.fromisoformat("2020-01-01")
    assert db.adapt_date(date) == "2020-01-01"

@pytest.mark.describe("adapt_datetime")
@pytest.mark.it("datetime.datetime を timezone-naive ISO 8601 datetime に変換する")
def test_adapt_datetime():
    dt = datetime.datetime.fromisoformat("2020-01-01T00:00:00")
    assert db.adapt_datetime(dt) == "2020-01-01T00:00:00"

@pytest.mark.describe("convert_date")
@pytest.mark.it("ISO 8601 date を datetime.date object に変換する")
def test_convert_date():
    date = datetime.date.today()
    iso_date = date.isoformat()
    assert db.convert_date(iso_date.encode()) == date

@pytest.mark.describe("convert_datetime")
@pytest.mark.it("ISO 8601 datetime を datetime.datetime object に変換する")
def test_convert_datetime():
    dt = datetime.datetime.now()
    iso_dt = dt.isoformat()
    assert db.convert_datetime(iso_dt.encode()) == dt

@pytest.mark.describe("convert_timestamp")
@pytest.mark.it("timestamp を datetime.datetime object に変換する")
def test_convert_timestamp():
    timestamp = datetime.datetime.now().timestamp()
    assert db.convert_timestamp(str(int(timestamp)).encode()) == datetime.datetime.fromtimestamp(int(timestamp))