from pydantic import BaseModel, Field

class GeneratorTextToImageData(BaseModel):
    """
    Text to Imageのリクエストデータ
    """
    prompt: str