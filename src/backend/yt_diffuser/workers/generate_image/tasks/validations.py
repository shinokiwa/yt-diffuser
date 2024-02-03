"""
生成処理のバリデーション定義
いろんなところから参照するので独立
"""
from pydantic import BaseModel, ValidationError

class TextToImageRequest(BaseModel):
    output_dir: str
    filename: str = "" # 出力ファイル名。空文字の場合は自動生成する。
    generate_count: int = 1

    seed: int = None
    width: int
    height: int

    prompt: str = None
    negative_prompt: str = None
    scheduler: str
    inference_steps: int
    guidance_scale: float

class ImageToImageRequest(TextToImageRequest):
    strength: float = 0.3
