from pydantic import BaseModel, Field

class GeneratorLoadData(BaseModel):
    """
    loadのリクエストデータ

    Pydanticの都合、model_から始まる名前は使えない点に注意
    """
    base_model_id: str
    base_revision: str
    compile: bool