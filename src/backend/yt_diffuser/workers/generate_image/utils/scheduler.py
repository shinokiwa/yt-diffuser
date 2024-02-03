"""
スケジューラをセットする

インポート関係がややこしいので独立
"""
import logging; logger = logging.getLogger(__name__)
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


def set_scheduler (pipe:StableDiffusionXLPipeline, scheduler:str) -> None:
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
    