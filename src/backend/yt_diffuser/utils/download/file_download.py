"""
hf_hub_downloadの定形処理をラッピングする。
"""
import logging; logger = logging.getLogger(__name__)

from huggingface_hub.file_download import hf_hub_download
from huggingface_hub.constants import REPO_TYPE_MODEL

# プログレスバーの非表示化
from huggingface_hub.utils import disable_progress_bars; disable_progress_bars()

from yt_diffuser.config import AppConfig

def hf_hub_file_download(
    config:AppConfig,
    repo_id: str,
    filename: str,
    *,
    revision: str = None
)-> str:

    offline = config.offline == True

    return hf_hub_download(
        repo_id, filename,

        repo_type=REPO_TYPE_MODEL,
        revision=revision,
        cache_dir=config.STORE_HF_MODEL_DIR,

        local_files_only=offline,

        resume_download=True,
        force_download=False,
        proxies=None,
        local_dir_use_symlinks="auto",
        use_auth_token=None,
        #user_agent=user_agent,
        subfolder=None,
    )
