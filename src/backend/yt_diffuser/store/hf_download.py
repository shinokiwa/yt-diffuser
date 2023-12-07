""" HuggingFace Hub からダウンロードするモジュール
"""
import sys
import os
import json
from requests import HTTPError
import time
from pathlib import Path

from tqdm import tqdm

from huggingface_hub import hf_hub_download, snapshot_download
from huggingface_hub.utils import EntryNotFoundError, RepositoryNotFoundError, RevisionNotFoundError

# プログレスバーは表示しない
from huggingface_hub.utils import disable_progress_bars; disable_progress_bars()

from huggingface_hub.file_download import repo_folder_name

class DownloadProgress(tqdm):
    """ ダウンロードの進捗表示
    """

    def display(self, msg: str | None = None, pos: int | None = None) -> None:
        """ 進捗表示
        シンプルに 現在の進捗 / 総数 を表示するだけ。

        params:
            msg: 進捗メッセージ。使用しない。
            pos: 進捗バーの位置。使用しない。
        """
        print (f"{self.n}/{self.total}")

        return True

def model_download(cache_dir:str, repo_id:str, revision:str, test_flg:str) -> None:
    """ モデルをダウンロードする

    args:
        cache_dir: キャッシュディレクトリ
        model_name: モデル名
        revision: リビジョン
        test_flg: テストフラグ、1の場合は実際にはダウンロードしない
    """

    repo_type = "model"

    # テストフラグが立っている場合はダウンロードしない
    if test_flg == "1":
        for i in DownloadProgress(range(10)):
            time.sleep(0.1)
        Path([cache_dir, repo_folder_name(repo_id, revision)]).mkdir(parents=True, exist_ok=True)
        return
    
    if repo_id == "" or cache_dir == "" or revision == "":
        raise ValueError("model_name, cache_dir, revision must be set")

    try:
        # Load from URL or cache if already cached
        config_file = hf_hub_download(
            repo_id,
            repo_type=repo_type,
            filename="model_index.json",
            cache_dir=cache_dir,
            force_download=False,
            proxies=None,
            resume_download=False,
            local_files_only=None,
            use_auth_token=None,
            #user_agent=user_agent,
            subfolder=None,
            revision=revision,
        )
    except (
        RepositoryNotFoundError,
        RevisionNotFoundError,
        EntryNotFoundError,
        HTTPError,
        ValueError,
        EnvironmentError
    ) as e:
        print (e.__class__.__name__)
        return

    with open(config_file, "r", encoding="utf-8") as reader:
        text = reader.read()

    config_dict = json.loads(text)

    folder_names = [k for k in config_dict.keys() if not k.startswith("_")]
    allow_patterns = [os.path.join(k, "*") for k in folder_names]
    allow_patterns += [
        "diffusion_pytorch_model.bin",  # WEIGHTS_NAME 
        "config.json",                  # CONFIG_NAME 
        "scheduler_config.json",        # SCHEDULER_CONFIG_NAME
        "model.onnx",                   # ONNX_WEIGHTS_NAME
        "model_index.json",             # PIPELINE_CONFIG_NAME
    ]

    # make sure we don't download flax weights
    ignore_patterns = "*.msgpack"

    # 必要な全ファイルをダウンロード
    snapshot_download(
        repo_id,
        cache_dir=cache_dir,
        resume_download=False,
        proxies=None,
        local_files_only=False,
        use_auth_token=None,
        revision=revision,
        allow_patterns=allow_patterns,
        ignore_patterns=ignore_patterns,
        #user_agent=user_agent,
        tqdm_class=DownloadProgress
    )


if __name__ == '__main__':
    # コマンドライン引数が引数になる
    model_download(*sys.argv[1:])