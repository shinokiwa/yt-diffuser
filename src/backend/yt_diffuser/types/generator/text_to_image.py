from pydantic import BaseModel, Field

class GeneratorTextToImageData(BaseModel):
    """
    Text to Imageのリクエストデータ
    """
    generate_count: int
    prompt: str
    negative_prompt: str
    scheduler: str