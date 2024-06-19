from typing import Optional

from pydantic import BaseModel

class GeneratorArgsTextToImage(BaseModel):
    """
    TEXT_TO_IMAGEコマンドへの引数
    """
    generate_count: int

    height: int
    width: int
    seed: Optional[int] = None

    prompt: str
    negative_prompt: str

    scheduler: str
    inference_steps: int
    guidance_scale: float