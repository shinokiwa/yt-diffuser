from typing import List
from pathlib import Path

from injector import inject

from yt_diffuser.types.path import AppPath


class TempImageUseCase:
    """
    一時保存画像のユースケース
    """

    @inject
    def __init__(self, path:AppPath):
        """
        コンストラクタ

        Args:
            path (AppPath): パス
        """
        self.path:Path = path.OUTPUT_TEMP_DIR

    def get_index(self) -> List[str]:
        """
        一時保存画像の一覧を取得する。
        """
        self.path.mkdir(parents=True, exist_ok=True)
        list = [str(p.relative_to(self.path)) for p in self.path.glob('*')]
        list = sorted(list, reverse=True)
        return list
