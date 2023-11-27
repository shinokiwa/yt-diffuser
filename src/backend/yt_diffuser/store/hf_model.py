""" HuggingFaceモデルストア
"""
import os
import json
from sqlite3 import Connection
from typing import Optional

from tqdm.auto import tqdm
from huggingface_hub import hf_hub_download, snapshot_download
from huggingface_hub.file_download import repo_folder_name
from huggingface_hub.utils import EntryNotFoundError, RepositoryNotFoundError, RevisionNotFoundError
from requests import HTTPError

# プログレスバーは表示しない
from huggingface_hub.utils import disable_progress_bars; disable_progress_bars()

from yt_diffuser.constant import STORE_HF_MODEL_DIRNAME
from yt_diffuser.store.model import ModelStore
from backend.yt_diffuser.store.db.op.models import is_exists_by_pathname, insert, update_by_pathname

class HFModelStore(ModelStore):
    """ HuggingFaceモデルストアクラス
    """
    config_name: str = "model_index.json"

    conn: Connection = None
    repo_id: str = ""
    revision: str = ""

    def __init__(self, conn:Connection, repo_id: str, revision: str):

        self.conn = conn
        self.repo_id = repo_id
        self.revision = revision

        path = STORE_HF_MODEL_DIRNAME + "/" + repo_folder_name(repo_id, revision)

        super().__init__(path)
    
    def download(self) -> None:
        """ モデルをダウンロードする
        """
        self.mkdir()
        if self.is_locked():
            raise EnvironmentError(f"{self.repo_id} is locked")

        self.lock()

        try:
            self._download()
            if is_exists_by_pathname(self.conn, self.path):
                update_by_pathname(self.conn, self.path,
                    name=self.repo_id,
                    revision=self.revision,
                    class_name=self.__class__.__name__
                )
            else:
                insert(self.conn,
                    path_name=self.path,
                    name=self.repo_id,
                    revision=self.revision,
                    class_name=self.__class__.__name__
                )
            self.conn.commit()

        except Exception as e:
            self.conn.rollback()

        finally:
            self.unlock()

    def _download(self, tqdm_class: Optional[tqdm] = None) -> None:
            try:
                # Load from URL or cache if already cached
                config_file = hf_hub_download(
                    self.repo_id,
                    filename=self.config_name,
                    cache_dir=self.base_dir,
                    force_download=False,
                    proxies=None,
                    resume_download=False,
                    local_files_only=None,
                    use_auth_token=None,
                    #user_agent=user_agent,
                    subfolder=None,
                    revision=self.revision,
                )
            except RepositoryNotFoundError:
                raise EnvironmentError(
                    f"{self.repo_id} is not a local folder and is not a valid model identifier"
                    " listed on 'https://huggingface.co/models'\nIf this is a private repository, make sure to pass a"
                    " token having permission to this repo with `use_auth_token` or log in with `huggingface-cli"
                    " login`."
                )
            except RevisionNotFoundError:
                raise EnvironmentError(
                    f"{self.revision} is not a valid git identifier (branch name, tag name or commit id) that exists for"
                    " this model name. Check the model page at"
                    f" 'https://huggingface.co/{self.repo_id}' for available revisions."
                )
            except EntryNotFoundError:
                raise EnvironmentError(
                    f"{self.model_name} does not appear to have a file named {self.config_name}."
                )
            except HTTPError as err:
                raise EnvironmentError(
                    "There was a specific connection error when trying to load"
                    f" {self.model_name}:\n{err}"
                )
            except ValueError:
                raise EnvironmentError(
                    f"We couldn't connect to '{HUGGINGFACE_CO_RESOLVE_ENDPOINT}' to load this model, couldn't find it"
                    f" in the cached files and it looks like {self.repo_id} is not the path to a"
                    f" directory containing a {self.config_name} file.\nCheckout your internet connection or see how to"
                    " run the library in offline mode at"
                    " 'https://huggingface.co/docs/diffusers/installation#offline-mode'."
                )
            except EnvironmentError:
                raise EnvironmentError(
                    f"Can't load config for '{self.repo_id}'. If you were trying to load it from "
                    "'https://huggingface.co/models', make sure you don't have a local directory with the same name. "
                    f"Otherwise, make sure '{self.repo_id}' is the correct path to a directory "
                    f"containing a {self.config_name} file"
                )

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
                self.repo_id,
                cache_dir=self.base_dir,
                resume_download=False,
                proxies=None,
                local_files_only=False,
                use_auth_token=None,
                revision=self.revision,
                allow_patterns=allow_patterns,
                ignore_patterns=ignore_patterns,
                #user_agent=user_agent,
                tqdm_class=tqdm_class
            )

            return (config_dict, folder_names)    