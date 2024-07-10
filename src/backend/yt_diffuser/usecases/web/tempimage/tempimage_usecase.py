from typing import List
from pathlib import Path

from injector import inject

from yt_diffuser.types.path import AppPath
from yt_diffuser.utils.file_path import is_child

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

    def delete(self, filename:str):
        """
        一時保存画像を削除する。

        Args:
            filename (str): ファイル名
        """
        path = self.path / filename
        if is_child(self.path, path) and path.exists():
            path.unlink(True)