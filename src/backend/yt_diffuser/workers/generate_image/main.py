"""
現状Diffusersのreadmeサンプルまま。
"""
import multiprocessing
import logging; logger = logging.getLogger(__name__)

import torch
from diffusers import DiffusionPipeline
from diffusers import StableDiffusionXLPipeline
from diffusers import LCMScheduler

from yt_diffuser.config import AppConfig
from yt_diffuser.utils.event import GenerateStatusEvent
from yt_diffuser.workers.generate_image.text_to_image import text_to_image

def procedure(config:AppConfig,
                   model_name:str,
                   revision:str,
                   message_queue:multiprocessing.Queue,
                   input_queue:multiprocessing.Queue):
    """
    画像生成処理

    Args:
        config (AppConfig): 設定
        model_name (str): モデル名
        revisin (str): モデルのリビジョン
        message_queue (multiprocessing.Queue): この処理から出力されるメッセージを格納するキュー
        input_queue (multiprocessing.Queue): この処理への入力を格納するキュー
    """
    GenerateStatusEvent.send_process(message_queue, GenerateStatusEvent.Status.LOADING, label=f"{model_name}:{revision}")

    pipe:StableDiffusionXLPipeline = DiffusionPipeline.from_pretrained(
        pretrained_model_name_or_path=model_name,
        revision=revision,
        cache_dir=config.STORE_HF_MODEL_DIR,
        torch_dtype=torch.float16,
        use_safetensors=True,
        local_files_only=True,
        variant="fp16",
    )

    adapter_id = "latent-consistency/lcm-lora-sdxl"
    pipe.load_lora_weights(adapter_id,
        revision=revision,
        cache_dir=config.STORE_HF_MODEL_DIR,
        local_files_only=True,
        weight_name="pytorch_lora_weights.safetensors"
    )
    pipe.fuse_lora()
    pipe.scheduler = LCMScheduler.from_config(pipe.scheduler.config)

    pipe.enable_model_cpu_offload()

    while True:

        GenerateStatusEvent.send_process(message_queue, GenerateStatusEvent.Status.READY, label=f"{model_name}:{revision}")

        recv = input_queue.get()

        if recv is None:
            continue

        (message, data) = recv

        if message == "exit":
            GenerateStatusEvent.send_process(message_queue, GenerateStatusEvent.Status.EXIT)
            break
        
        if message == "text-to-image":

            text_to_image(pipe, config, message_queue, data)
            continue