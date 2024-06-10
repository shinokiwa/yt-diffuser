from typing import List
from logging import getLogger; logger = getLogger(__name__)

from injector import inject

from huggingface_hub import scan_cache_dir, HFCacheInfo

from yt_diffuser.types.path import AppPath

class ModelStore:
    """
    モデルストア
    ファイルシステム上のモデルを管理する
    """

    @inject
    def __init__(self, app_path:AppPath):
        """
        コンストラクタ
        """
        self.app_path = app_path
    
    def read (self) -> List[HFCacheInfo]:
        """
        モデル一覧を取得する
        """
        hf_cache_info = scan_cache_dir(self.app_path.STORE_HF_MODEL_DIR)
        return [hf_cache_info]