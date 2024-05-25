import logging; logger = logging.getLogger(__name__)
import datetime
import multiprocessing
from pathlib import Path

import torch
from diffusers import StableDiffusionXLPipeline, StableDiffusionXLInpaintPipeline
from diffusers.utils import load_image

from yt_diffuser.config import AppConfig
from yt_diffuser.utils.event import FilesystemEvent, GenerateProgressEvent

from .validations import ImageToImageRequest, ValidationError
from ..utils.scheduler import set_scheduler
from ..utils.tqdm import GenerateProgressTqdm
from ..utils.image_utils import save_image


def inpaint (
        pipe:StableDiffusionXLPipeline,
        config:AppConfig,
        input_queue:multiprocessing.Queue,
        message_queue:multiprocessing.Queue,
        model_name:str,
        req:dict
    ) -> None:
    """
    InPaintで画像を生成する。
    """
    logger.debug("Start inpaint process.")

    try:
        data = ImageToImageRequest(**req).dict()
    except ValidationError as e:
        raise e

    set_scheduler(pipe, data["scheduler"])
    output_dir = Path(data["output_dir"])

    inpaint_pipe = StableDiffusionXLInpaintPipeline(**pipe.components)

    elapsed_list = []
    i = 0
    average = 0
    for cnt in range(0, data["generate_count"]):
        tqdm = GenerateProgressTqdm(queue=message_queue, generate_total=data["generate_count"], generate_count=cnt, average=average)

        # 後でちゃんと実装するけど、とりあえず
        # progress_barを無理やり差し替える
        def progress_bar(iterable=None, total=None):
            if iterable is not None:
                tqdm.iterable = iterable
                tqdm.total = len(iterable) + 2
                return tqdm
            elif total is not None:
                tqdm.total = total + 2
                return tqdm
            else:
                raise ValueError("Either `total` or `iterable` has to be defined.")

        inpaint_pipe.progress_bar = progress_bar

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
            seed = data["seed"]
        else:
            seed = initial_seed.seed()

        initial_seed.manual_seed(seed)

        init_image = load_image(str(config.INPUT_SOURCE_FILE)).convert("RGB")
        mask_image = load_image(str(config.INPUT_MASK_FILE)).convert("RGB")

        image = inpaint_pipe(
            prompt=data["prompt"],
            negative_prompt=data["negative_prompt"],
            width=data["width"],
            height=data["height"],
            num_inference_steps=data["inference_steps"],
            generator=initial_seed,
            image=init_image,
            mask_image=mask_image,
            guidance_scale=data["guidance_scale"],
            strength=data["strength"],
        ).images[0]

        tqdm.update(1)

        save_image(image, output_path, model_name, seed, data)

        FilesystemEvent.send_process(message_queue, FilesystemEvent.Type.CREATE, str(output_path))

        tqdm.update(1)
        elapsed_list.append(tqdm.format_dict['elapsed'])
        average = sum(elapsed_list) / len(elapsed_list) if len(elapsed_list) > 0 else 0

    GenerateProgressEvent.send_process(
        process_queue=message_queue,
        generate_total=data["generate_count"],
        generate_count=data["generate_count"],

        steps_total=0,
        steps_count=0,

        percentage=0,
        elapsed=0,
        remaining=0,
        average=average
    )

