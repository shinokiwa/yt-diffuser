"""
現状Diffusersのreadmeサンプルまま。
"""
import datetime
import multiprocessing
import logging; logger = logging.getLogger(__name__)

import torch
from diffusers import DiffusionPipeline
from diffusers import StableDiffusionXLPipeline

from yt_diffuser.config import AppConfig
from yt_diffuser.utils.message_queue import send_message, send_progress, send_ready

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
    send_message(message_queue, 'genarate-load-start', target=f"{model_name}:{revision}")

    pipe:StableDiffusionXLPipeline = DiffusionPipeline.from_pretrained(
        pretrained_model_name_or_path=model_name,
        revision=revision,
        cache_dir=config.STORE_HF_MODEL_DIR,
        torch_dtype=torch.float16,
        use_safetensors=True,
        local_files_only=True,
        variant="fp16"
    )
    pipe.enable_model_cpu_offload()

    send_message(message_queue, 'genarate-load-complete', target=f"{model_name}:{revision}")
    send_ready(message_queue, "generate", f"{model_name}:{revision}")

    while True:
        recv = input_queue.get()

        if recv is None:
            continue

        (message, data) = recv

        if message == "exit":
            break
        
        if message == "generate-image":

            text = data['text']
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d-%H%M%S')
            config.OUTPUT_TEMP_DIR.mkdir(parents=True, exist_ok=True)
            # 出力ファイル名は末尾を4桁ゼロ埋めの連番にする
            i = 0
            output_path = None
            while True:
                output_path = config.OUTPUT_TEMP_DIR / f"{timestamp}-{i:04}.png"
                if not output_path.exists():
                    break
                i += 1

            send_message(message_queue, 'genarate-start', target=f"{timestamp}")

            image = pipe(text).images[0]

            image.save(output_path)

            send_message(message_queue, 'genarate-complete', target=output_path.name)
