from pydantic import BaseModel

from .project_layers import ProjectLayers

class Project(BaseModel):
    """
    プロジェクトの情報を保持するクラス
    """

    project_name: str
    height: int
    width: int
    version: int = 1

    layers: ProjectLayers = ProjectLayers()
