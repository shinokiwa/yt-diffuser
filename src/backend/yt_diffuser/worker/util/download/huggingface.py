""" HuggingFace Hub からダウンロードするモジュール
"""
# プログレスバーは表示しない
from huggingface_hub.utils import disable_progress_bars; disable_progress_bars()

from huggingface_hub import hf_hub_download, snapshot_download
from huggingface_hub.utils import EntryNotFoundError, RepositoryNotFoundError, RevisionNotFoundError
from requests import HTTPError

import os
import json

from yt_diffuser.worker.util.tqdm import WorkerProgress

def model_download():
    model_name = "stabilityai/stable-diffusion-xl-base-1.0"
    cache_dir = "/workspace/data/huggingface/"
    revision = "main"

    try:
        # Load from URL or cache if already cached
        config_file = hf_hub_download(
            model_name,
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
    except RepositoryNotFoundError:
        raise EnvironmentError(
            f"{model_name} is not a local folder and is not a valid model identifier"
            " listed on 'https://huggingface.co/models'\nIf this is a private repository, make sure to pass a"
            " token having permission to this repo with `use_auth_token` or log in with `huggingface-cli"
            " login`."
        )
    except RevisionNotFoundError:
        raise EnvironmentError(
            f"{revision} is not a valid git identifier (branch name, tag name or commit id) that exists for"
            " this model name. Check the model page at"
            f" 'https://huggingface.co/{model_name}' for available revisions."
        )
    except EntryNotFoundError:
        raise EnvironmentError(
            f"{model_name} does not appear to have a file named {cls.config_name}."
        )
    except HTTPError as err:
        raise EnvironmentError(
            "There was a specific connection error when trying to load"
            f" {model_name}:\n{err}"
        )
    except ValueError:
        raise EnvironmentError(
            f"We couldn't connect to '{HUGGINGFACE_CO_RESOLVE_ENDPOINT}' to load this model, couldn't find it"
            f" in the cached files and it looks like {model_name} is not the path to a"
            f" directory containing a {cls.config_name} file.\nCheckout your internet connection or see how to"
            " run the library in offline mode at"
            " 'https://huggingface.co/docs/diffusers/installation#offline-mode'."
        )
    except EnvironmentError:
        raise EnvironmentError(
            f"Can't load config for '{model_name}'. If you were trying to load it from "
            "'https://huggingface.co/models', make sure you don't have a local directory with the same name. "
            f"Otherwise, make sure '{model_name}' is the correct path to a directory "
            f"containing a {cls.config_name} file"
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
        model_name,
        cache_dir=cache_dir,
        resume_download=False,
        proxies=None,
        local_files_only=False,
        use_auth_token=None,
        revision=revision,
        allow_patterns=allow_patterns,
        ignore_patterns=ignore_patterns,
        #user_agent=user_agent,
        tqdm_class=WorkerProgress
    )

    return (config_dict, folder_names)