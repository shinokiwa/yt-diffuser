from injector import inject

from yt_diffuser.types.project import Project, ProjectLayer
from yt_diffuser.adapters.project.interface import IProjectDirectoryAdapter
from .project_usecase import ProjectUseCase

class ProjectLayerUseCase:
    """
    プロジェクトのレイヤーに関するユースケース
    """

    @inject
    def __init__(self, dir: IProjectDirectoryAdapter):
        self.dir = dir

    def is_exists(self, project: Project, layer_id: str) -> bool:
        """
        レイヤーが存在するか確認する
        """
        return project.layers.is_exists(layer_id)
    
    def add_layer(self, project:Project, layer_id: str) -> None:
        """
        レイヤーを追加する
        """
        if self.is_exists(project, layer_id):
            raise Exception(f"Layer {layer_id} already exists.")

        layer = ProjectLayer(layer_name=layer_id)
        self.dir.add_layer(project.project_name, layer.layer_id)

        project.layers.add_layer(layer_id)
        self.dir.update(project)
        return
