"""
HuggingFaceモデルストア
"""
from pathlib import Path

from huggingface_hub.file_download import repo_folder_name
from huggingface_hub.constants import REPO_TYPE_MODEL

# プログレスバーは表示しない
from huggingface_hub.utils import disable_progress_bars; disable_progress_bars()

from yt_diffuser.store.model import ModelStore, AppConfig
from yt_diffuser.store.db.op.models import MODEL_CLASS_NAME

class HFModelStore(ModelStore):
    """
    HuggingFaceモデルストアクラス
    """
    class_num: int = MODEL_CLASS_NAME['HFModelStore']

    def __init__(self, config:AppConfig,  repo_id: str, revision: str):
        super().__init__(config, repo_id, revision)
    
    @property
    def path(self) -> Path:
        return self.config.STORE_HF_MODEL_DIR / repo_folder_name(repo_id=self.store_name, repo_type=REPO_TYPE_MODEL)
    