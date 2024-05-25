"""
現状Diffusersのreadmeサンプルまま。
"""
import multiprocessing
import logging; logger = logging.getLogger(__name__)

import torch
import torch._inductor.config
from diffusers import DiffusionPipeline
from diffusers import StableDiffusionXLPipeline
from diffusers import LCMScheduler, EulerDiscreteScheduler

from yt_diffuser.config import AppConfig
from yt_diffuser.utils.event import GenerateStatusEvent

from .tasks.text_to_image import text_to_image
from .tasks.image_to_image import image_to_image
from .tasks.inpaint import inpaint
from .tasks.compile import compile_current_model

def procedure(
        config:AppConfig,
        model_name:str,
        revision:str,
        compile:bool,
        message_queue:multiprocessing.Queue,
        input_queue:multiprocessing.Queue
    ):
    """
    画像生成処理

    Args:
        config (AppConfig): 設定
        model_name (str): モデル名
        revisin (str): モデルのリビジョン
        message_queue (multiprocessing.Queue): この処理から出力されるメッセージを格納するキュー
        input_queue (multiprocessing.Queue): この処理への入力を格納するキュー
    """
    if config.debug:
        logging.basicConfig(level=logging.DEBUG)

    adapter_id = "latent-consistency/lcm-lora-sdxl"

    lora_model_label = ""
    GenerateStatusEvent.send_process(message_queue, GenerateStatusEvent.Status.LOADING,
        base_model_label=f"{model_name}({revision}):fp16",
        lora_model_label=lora_model_label
    )

    pipe:StableDiffusionXLPipeline = DiffusionPipeline.from_pretrained(
        pretrained_model_name_or_path=model_name,
        revision=revision,
        cache_dir=config.STORE_HF_MODEL_DIR,
        torch_dtype=torch.bfloat16,
        use_safetensors=True,
        local_files_only=True,
        variant="fp16",
    )

    if torch.cuda.is_available():
        pipe = pipe.to("cuda")

    if compile:
        compile_current_model(pipe)

    while True:

        GenerateStatusEvent.send_process(message_queue, GenerateStatusEvent.Status.READY,
            base_model_label=f"{model_name}({revision}):fp16",
            lora_model_label=lora_model_label
        )

        recv = input_queue.get()

        if recv is None:
            continue

        (message, data) = recv

        if message == "exit":
            GenerateStatusEvent.send_process(message_queue, GenerateStatusEvent.Status.EXIT)
            break
        
        if message == "load-lora":
            pipe.load_lora_weights(adapter_id,
                revision=revision,
                cache_dir=config.STORE_HF_MODEL_DIR,
                local_files_only=True,
                weight_name="pytorch_lora_weights.safetensors"
            )
            lora_model_label = f"{adapter_id}({revision}):pytorch_lora_weights.safetensors"
            pipe.scheduler = LCMScheduler.from_config(pipe.scheduler.config)
            continue

        if message == "remove-lora":
            pipe.unload_lora_weights()
            lora_model_label = ""
            pipe.scheduler = EulerDiscreteScheduler.from_config(pipe.scheduler.config)
            continue
        
        if message == "text-to-image":

            try:
                text_to_image(
                    pipe,
                    config,
                    input_queue,
                    message_queue,
                    model_name,
                    data
                )
            except Exception as e:
                logger.exception(e)
                GenerateStatusEvent.send_process(message_queue, GenerateStatusEvent.Status.ERROR, error=str(e))

            continue

        if message == "image-to-image":

            try:
                image_to_image(
                    pipe,
                    config,
                    input_queue,
                    message_queue,
                    model_name,
                    data
                )
            except Exception as e:
                logger.exception(e)
                GenerateStatusEvent.send_process(message_queue, GenerateStatusEvent.Status.ERROR, error=str(e))

            continue

        if message == "inpaint":

            try:
                inpaint(
                    pipe,
                    config,
                    input_queue,
                    message_queue,
                    model_name,
                    data
                )
            except Exception as e:
                logger.exception(e)
                GenerateStatusEvent.send_process(message_queue, GenerateStatusEvent.Status.ERROR, error=str(e))

            continue