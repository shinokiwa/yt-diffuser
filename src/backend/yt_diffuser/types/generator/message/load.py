from pydantic import BaseModel

class GeneratorArgsLoad(BaseModel):
    """
    LOADコマンドへの引数
    """
    base_model_id: str
    base_revision: str
    compile: bool
