"""
パス定義
"""
from typing import Union
from pathlib import Path

class AppPath:
    """
    パス定義
    """

    def __init__(self, base_dir: str = None, db_file: str = None) -> None:
        """
        コンストラクタ
        """

        self.BASE_DIR: Path = Path(__file__).parents[4] if base_dir is None else Path(base_dir)
        """
        ベースディレクトリ
        """


        self.DATA_DIR: Path = self.BASE_DIR / "data"

        # ストア関連
        self.STORE_DIR: Path  = self.DATA_DIR / "store"
        self.STORE_MODEL_DIR: Path = self.STORE_DIR / "models"
        self.STORE_HF_MODEL_DIR: Path = self.STORE_MODEL_DIR / "huggingface"

        # データベース関連
        self.DB_FILE: Union[Path, str] = self.DATA_DIR / "db/yt_diffuser.sqlite3" if db_file is None else db_file

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