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
                 DB_FILE:Union[Path, str]=None,
                 offline:bool=False
                 ) -> None:
        """
        コンストラクタ

        一部の設定値は引数によりオーバーライド可能。

        Args:
            debug: デバッグモード
            BASE_DIR: ベースディレクトリ
            DB_FILE: データベースファイル
            offline: オフラインモード
        """

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
        self.STORE_LAST_USED_MODEL_DIR: Path = self.STORE_MODEL_DIR / "lastused"

        # データベース関連
        self.DB_FILE: Union[str, Path] = self.DATA_DIR / "db/yt_diffuser.sqlite3"
        if DB_FILE is not None:
            self.DB_FILE = DB_FILE

        # 出力データ関連
        self.OUTPUT_DIR: Path = self.DATA_DIR / "output"
        self.OUTPUT_TEMP_DIR: Path = self.OUTPUT_DIR / "temp"
        self.OUTPUT_IMAGE_DIR: Path = self.OUTPUT_DIR / "images"
        self.OUTPUT_PREVIEW_PATH: Path = self.OUTPUT_DIR / "preview/preview.png"

        # 入力データ関連
        self.INPUT_DIR: Path = self.DATA_DIR / "input"
        self.INPUT_SOURCE_FILE: Path = self.INPUT_DIR / "source.png"
        self.INPUT_MASK_FILE: Path = self.INPUT_DIR / "mask.png"
        self.INPUT_CONTROLNET_FILE: Path = self.INPUT_DIR / "controlnet.png"