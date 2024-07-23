from injector import inject

from yt_diffuser.types.project import Project, ProjectLayer
from yt_diffuser.adapters.project.interface import IProjectLayerRepository

class ProjectLayerUseCase:
    """
    プロジェクトのレイヤーに関するユースケース
    """

    @inject
    def __init__(self, layer_repository: IProjectLayerRepository):
        self.layer_repository = layer_repository

    def is_exists(self, project_name: str, layer: ProjectLayer) -> bool:
        """
        レイヤーが存在するか確認する
        """
        return self.layer_repository.is_exists(project_name, layer)
    
    def add_layer(self, project_name:str, layer: ProjectLayer) -> None:
        """
        レイヤーを追加する
        """
        if self.is_exists(project_name, layer):
            raise Exception(f"Layer {layer.layer_id} already exists.")

        self.layer_repository.create(project_name, layer)
        return

    def upload_image(self, project_name:str, layer_id:str, file_name:str, source_path:str) -> None:
        """
        画像をアップロードする
        """
        self.layer_repository.save_image(project_name, layer_id, file_name, source_path, is_copy=False)
        return