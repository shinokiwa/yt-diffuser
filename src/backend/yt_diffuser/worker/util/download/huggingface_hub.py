



# とりあえず参考用に過去分コピー
import os

from diffusers.configuration_utils import ConfigMixin

from huggingface_hub.utils import disable_progress_bars; disable_progress_bars()
from huggingface_hub import snapshot_download, REPO_TYPE_MODEL
from huggingface_hub.file_download import repo_folder_name
from diffusers.utils.hub_utils import http_user_agent

class ConfigLoader(ConfigMixin):
    config_name = "model_index.json"
    _optional_components = []

def hf_download_model (cache_dir:str, model_name:str, revision:str):
    """必要に応じてHuggingFaceからモデルをダウンロードする
    """
    # model_index.json のみダウンロード
    config_dict = ConfigLoader.load_config(
        model_name,
        cache_dir=cache_dir,
        resume_download=False,
        force_download=False,
        proxies=None,
        local_files_only=False,
        use_auth_token=None,
        revision=revision,
    )

    # make sure we only download sub-folders and `diffusers` filenames
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
    user_agent = {"pipeline_class": "StableDiffusionPipeline"}
    user_agent = http_user_agent(user_agent)

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
        user_agent=user_agent,
    )
    return True

def hf_load_models (cache_dir, model_name, revision):
    """HuggingFaceからダウンロードしたモデルファイルをロードする
    """

    cached_dir = hf_get_cached_dir(cache_dir, model_name, revision)

    if os.path.isdir(cached_dir):
        config_dict = ConfigLoader.load_config(cached_dir)
        config_dict["cached_folder"] = cached_dir
    else:
        raise FileNotFoundError( f'Model "{cached_dir}" is Not Found.')
    return config_dict

def hf_get_cached_dir (cache_dir, model_name, revision):
    """HuggingFaceからダウンロードするモデルファイルのパスを取得する

    Args:
        model_name (_type_): _description_
        revision (_type_): _description_
    """
    storage_dir = os.path.join(
        cache_dir, repo_folder_name(repo_id=model_name, repo_type=REPO_TYPE_MODEL)
    )
    ref_path = os.path.join(storage_dir, "refs", revision)
    with open(ref_path) as f:
        commit_hash = f.read()

    snapshot_dir = os.path.join(storage_dir, "snapshots", commit_hash)
    return snapshot_dir


import logging
logger = logging.getLogger(__name__)

from pydantic import BaseModel, ValidationError

from yt_stablediffusion import path
from yt_stablediffusion.webapi import api, APIResponse

from yt_stablediffusion.pipelines import PipelineManager
from yt_stablediffusion.pipelines.hf_utils import hf_download_model

class InputAPIModelHFDownload(BaseModel):
    """GETの入力値クラス
    """
    type:str
    username:str
    modelname:str
    revision:str

@api.get('/api/model/hf/<type>/<username>/<modelname>/<revision>')
def api_model_hf_download(type:str, username:str, modelname:str, revision:str):
    """HuggingFaceから画像生成モデルをダウンロードするAPI

    Args:
        form (dict): form

    Returns:
        _type_: _description_
    """
    res = APIResponse()
    # 入力チェック
    try:
        i = InputAPIModelHFDownload(
            type=type,
            username=username,
            modelname=modelname,
            revision=revision
        )
    except  ValidationError as e:
        return res.err_validation(e.errors())

    cache_dir = path.dir_by_model_type(i.type)
    if cache_dir is None:
        return res.err_validation([f'Type {i.type} is not supported.'])

    model = f'{i.username}/{i.modelname}'

    pm = PipelineManager.get_instance()
    if pm.status.processing:
        return res.block()

    # 以降は非同期のブロッキング処理
    def proc ():
        # モデルのダウンロード
        hf_download_model(
            cache_dir=cache_dir,
            model_name=model,
            revision=i.revision
        )
        return None
    
    pm.make_pipeline(pm.status.set_download, proc)
    return res.ok()