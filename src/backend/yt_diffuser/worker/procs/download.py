""" ダウンロードのプロシージャ
"""

from yt_diffuser.store.db import connect_database
from yt_diffuser.store.hf_model import HFModelStore

def download_procedure() -> None:
    """ ダウンロードのプロシージャ
    """
    conn = connect_database()
    hf_model_store = HFModelStore(conn, repo_id="CompVis/stable-diffusion-v1-4", revision="fp16")
    hf_model_store.download()