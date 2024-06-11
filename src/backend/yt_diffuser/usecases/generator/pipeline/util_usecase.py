import logging; logger = logging.getLogger(__name__)
from typing import Dict, Tuple

import torch
from injector import inject
from diffusers import (
    StableDiffusionXLPipeline,

    DDIMScheduler,
    PNDMScheduler,
    DEISMultistepScheduler,
    DPMSolverSinglestepScheduler,
    DPMSolverMultistepScheduler,
    EulerDiscreteScheduler,
    EulerAncestralDiscreteScheduler,
    LCMScheduler
)

from PIL import Image
from PIL.PngImagePlugin import PngInfo
from pathlib import Path
import json


class PipelineUtilUseCase:
    """
    パイプラインのユーティリティを提供するユースケース
    """

    @inject
    def __init__(self):
        pass

    def init_seed_generator(self, pipeline, input_seed=None) -> Tuple[int, torch.Generator]:
        """
        SEED値の初期化とGeneratorの生成

        """
        # SEED値の設定
        initial_seed = torch.Generator(device=pipeline.device)
        if input_seed is None:
            seed = initial_seed.seed()
        else:
            seed = input_seed

        return (seed, initial_seed.manual_seed(seed))


    def save_image(self, image:Image, filepath:Path, model_name, seed, data:Dict):
        metadata = PngInfo()
        metadata.add_text('Title', 'AI generated image')
        metadata.add_text('Description', data.get('prompt', ''))
        metadata.add_text('Software', 'YuTori Diffuser')
        metadata.add_text('Source', model_name)
        comment = {
            "uc": data.get('negative_prompt', ''),
            "seed": seed,
        }
        if 'steps' in data:
            comment['steps'] = data.get('steps')

        if 'sampler' in data:
            comment['sampler'] = data.get('scheduler')

        if 'strength' in data:
            comment['strength'] = data.get('strength')

        if 'guidance_scale' in data:
            comment['scale'] = data.get('guidance_scale')

        metadata.add_text('Comment', json.dumps(comment))
        image.save(filepath, pnginfo=metadata)


    def set_scheduler (self, pipe:StableDiffusionXLPipeline, scheduler:str) -> None:
        if scheduler == "ddim":
            pipe.scheduler = DDIMScheduler.from_config(pipe.scheduler.config)
        elif scheduler == "pndm":
            pipe.scheduler = PNDMScheduler.from_config(pipe.scheduler.config)
        elif scheduler == "deis":
            pipe.scheduler = DEISMultistepScheduler.from_config(pipe.scheduler.config)
        elif scheduler == "dpms-singlestep":
            pipe.scheduler = DPMSolverSinglestepScheduler.from_config(pipe.scheduler.config)
        elif scheduler == "dpms-multistep":
            pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
        elif scheduler == "euler":
            pipe.scheduler = EulerDiscreteScheduler.from_config(pipe.scheduler.config)
        elif scheduler == "euler-ancestral":
            pipe.scheduler = EulerAncestralDiscreteScheduler.from_config(pipe.scheduler.config)
        elif scheduler == "lcm":
            pipe.scheduler = LCMScheduler.from_config(pipe.scheduler.config)
        else:
            raise ValueError(f"invalid scheduler: {scheduler}")
        logger.debug(f"set scheduler: {scheduler}")