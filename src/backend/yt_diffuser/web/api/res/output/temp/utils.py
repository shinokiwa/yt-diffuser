"""
一時保存リソース関係のAPI 共通処理
"""
from pathlib import Path
from datetime import datetime

from pydantic import BaseModel, ValidationError, Field
from pydantic.error_wrappers import ErrorWrapper

from yt_diffuser.web.api.res.output.utils import is_child

class PostTempRequest(BaseModel):
    """
    POSTリクエストのバリデーション
    """
    target: str = Field(default_factory=lambda: datetime.now().strftime('%Y-%m-%d %H-%M-%S'))

    def get_full_target (self, base_dir:Path):
        """
        ターゲットのフルパスを取得する。
        
        raise:
            ValidationError: ターゲットがベースディレクトリより上にある場合
        """
        target = Path(self.target)
        full_target = (base_dir / target).resolve()

        if not is_child(base_dir, full_target):
            raise ValidationError([
                ErrorWrapper(
                    ValueError('invalid path'),
                    loc=('target',)
                )
            ], self)
        
        return full_target


def get_temp_file_path (base_dir:Path, subpath:str):
    """
    subpathから一時保存中ファイルのフルパスを取得する。
    共通チェックも兼ねる。

    raise:
        ValidationError: ファイルが存在しない場合、ファイルでない場合
    """
    request_file = (base_dir / subpath).resolve()

    # ファイルが存在しない場合はエラー
    # ファイルでない場合はエラー
    # subpathがベースディレクトリより上にある場合はエラー
    if not request_file.exists() \
        or not request_file.is_file() \
        or not is_child(base_dir, request_file):
        raise ValueError('invalid path')

    return request_file
