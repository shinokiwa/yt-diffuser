import datetime
import multiprocessing
from pathlib import Path

import torch
from diffusers import StableDiffusionXLPipeline

from yt_diffuser.config import AppConfig
from yt_diffuser.utils.event import FilesystemEvent
from yt_diffuser.workers.generate_image.validations import TextToImageRequest, ValidationError
from yt_diffuser.workers.generate_image.scheduler import set_scheduler

def text_to_image (
        pipe:StableDiffusionXLPipeline,
        config:AppConfig,
        message_queue:multiprocessing.Queue,
        req:dict) -> None:
    """
    Text to Imageで画像を生成する。
    """

    try:
        data = TextToImageRequest(**req).dict()
    except ValidationError as e:
        raise e

    set_scheduler(pipe, data["scheduler"])
    output_dir = Path(data["output_dir"])

    pipe

    i = 0
    for cnt in range(0, data["generate_count"]):

        if data["filename"] == "":
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d-%H%M%S')
            while True:
                filename = f"{timestamp}-{i:04}.png"
                
                if not (output_dir / filename).exists():
                    break
                else:
                    i += 1
        else:
            filename = data["filename"]
        
        output_path = output_dir / filename

        initial_seed = torch.Generator(device="cpu")
        if data["seed"] is not None:
            initial_seed.manual_seed(data["seed"])
        else:
            initial_seed.manual_seed(torch.Generator(device="cpu").seed())
        image = pipe(
            prompt=data["prompt"],
            negative_prompt=data["negative_prompt"],
            width=data["width"],
            height=data["height"],
            num_inference_steps=data["inference_steps"],
            generator=initial_seed,
            guidance_scale=data["guidance_scale"]
        ).images[0]

        image.save(output_path)

        FilesystemEvent.send_process(message_queue, FilesystemEvent.Type.CREATE, str(output_path))
