""" アプリケーション設定値
"""
from typing import Union
from pathlib import Path

class AppConfig:
    """ アプリケーション設定値
    """

    def __init__(self,
                 debug:bool=False,
                 BASE_DIR:Union[Path, str]=None,
                 offline:bool=False
                 ) -> None:
        """
        コンストラクタ

        一部の設定値は引数によりオーバーライド可能。

        Args:
            debug: デバッグモード
            BASE_DIR: ベースディレクトリ
            offline: オフラインモード
        """

        #### 都度変更する可能性のある設定値 ####

        self.DB_VERSION = 1
        """
        DBのバージョン値
        この値がDBに保存されているバージョン値より大きい場合、DBのセットアップが必要
        この値は、DBの構成バージョンであり、アプリケーションのバージョンとは異なる
        """


        #### 基本的に変更されない設定値 ####
        self.debug: bool = debug
        """
        デバッグモード
        """

        self.offline: bool = offline
        """
        オフラインモード
        主にテスト用で、ネットワークからモデルをダウンロードしない。
        """

        self.BASE_DIR: Path = Path(__file__).parents[3] if BASE_DIR is None else Path(BASE_DIR)
        """
        ベースディレクトリ
        """

        self.DATA_DIR: Path = self.BASE_DIR / "data"

        # ストア関連
        self.STORE_DIR: Path  = self.DATA_DIR / "store"
        self.STORE_MODEL_DIR: Path = self.STORE_DIR / "models"
        self.STORE_HF_MODEL_DIR: Path = self.STORE_MODEL_DIR / "huggingface"

        # データベース関連
        self.DB_DIR: Path = self.DATA_DIR / "db"
        self.DB_FILE: Path = self.DB_DIR / "yt_diffuser.db"
        self.DB_UPDATE_FILE: Path = self.DB_DIR /"yt_diffuser_update.db"

        # 出力データ関連
        self.OUTPUT_DIR: Path = self.DATA_DIR / "output"
        self.OUTPUT_TEMP_DIR: Path = self.OUTPUT_DIR / "temp"
        self.OUTPUT_IMAGE_DIR: Path = self.OUTPUT_DIR / "images"
        self.OUTPUT_PREVIEW_PATH: Path = self.OUTPUT_DIR / "preview/preview.png"