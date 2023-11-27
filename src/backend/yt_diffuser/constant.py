""" 定数定義
"""
import os
from pathlib import Path


# パス関連
BASE_DIR: Path = Path(__file__).parents[3]

if os.environ.get("TEST") == "1":
    import tempfile
    BASE_DIR = Path(tempfile.gettempdir()) / "yt_diffuser_test"

DATA_DIR: Path = BASE_DIR / "data"

if os.environ.get("YT_DIFFUSER_DATA_DIR", "") != "":
    DATA_DIR = Path(os.environ["YT_DIFFUSER_DATA_DIR"])

# ストア関連
STORE_DIR: Path  = DATA_DIR / "store"
STORE_MODEL_DIR: Path = STORE_DIR / "model"
STORE_HF_MODEL_DIRNAME: str = "hf"
STORE_LOCK_FILE: str = ".lock"

# データベース関連
DB_DIR: Path = DATA_DIR / "db"
DB_FILE: Path = DB_DIR / "yt_diffuser.db"
DB_UPDATE_FILE: Path = DB_DIR /"yt_diffuser_update.db"

DB_VERSION = 1
"""DBのバージョン値
この値がDBに保存されているバージョン値より大きい場合、DBのセットアップが必要
この値は、DBの構成バージョンであり、アプリケーションのバージョンとは異なる
"""
