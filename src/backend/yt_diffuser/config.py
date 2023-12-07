""" アプリケーション設定値
"""
import os
from pathlib import Path

class AppConfig:
    """ アプリケーション設定値
    """

    def __init__(self, **kwargs) -> None:
        """ コンストラクタ
        """

        #### 都度変更する可能性のある設定値 ####

        self.DB_VERSION = 1
        """DBのバージョン値
        この値がDBに保存されているバージョン値より大きい場合、DBのセットアップが必要
        この値は、DBの構成バージョンであり、アプリケーションのバージョンとは異なる
        """


        #### 基本的に変更されない設定値 ####
        self.BASE_DIR: Path = Path(__file__).parents[3] if kwargs.get("BASE_DIR") is None else Path (kwargs.get("BASE_DIR"))

        self.DATA_DIR: Path = self.BASE_DIR / "data"

        # ストア関連
        self.STORE_DIR: Path  = self.DATA_DIR / "store"
        self.STORE_MODEL_DIR: Path = self.STORE_DIR / "model"
        self.STORE_HF_MODEL_DIR: Path = self.STORE_MODEL_DIR / "huggingface"

        # データベース関連
        self.DB_DIR: Path = self.DATA_DIR / "db"
        self.DB_FILE: Path = self.DB_DIR / "yt_diffuser.db"
        self.DB_UPDATE_FILE: Path = self.DB_DIR /"yt_diffuser_update.db"
