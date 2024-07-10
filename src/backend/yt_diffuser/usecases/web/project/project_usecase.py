from injector import inject

from yt_diffuser.types.project import Project, ProjectLayer
from yt_diffuser.adapters.project.interface import IProjectDirectoryAdapter

class ProjectUseCase:
    """
    プロジェクトに関するユースケース
    """

    @inject
    def __init__(self, dir: IProjectDirectoryAdapter):
        self.dir = dir

    def is_exists(self, name: str) -> bool:
        """
        プロジェクトが存在するか確認する
        """
        return self.dir.is_exists(name)

    def create_project(self, name: str, width: int, height: int) -> None:
        """
        プロジェクトを作成する
        """
        project = Project(project_name=name, width=width, height=height)
        if self.is_exists(name):
            raise Exception(f"Project {name} already exists.")
        
        self.dir.create(project)
        return
    
    def get_project(self, name: str) -> Project:
        """
        プロジェクトを取得する
        """
        return self.dir.get_project(name)
    
    def remove_project(self, name: str) -> None:
        """
        プロジェクトを削除する
        """
        self.dir.remove(name)
        return
    
    def get_project_list(self) -> list:
        """
        プロジェクトのリストを取得する
        """
        return self.dir.get_list()
    
    def add_layer(self, project_name: str, layer_name: str) -> None:
        """
        レイヤーを追加する
        """
        project = self.get_project(project_name)
        if project.layers.is_exists(layer_name):
            raise Exception(f"Layer {layer_name} already exists.")

        layer = ProjectLayer(layer_name=layer_name)
        self.dir.add_layer(project.project_name, layer.layer_id)

        project.layers.add_layer(layer_name)
        self.dir.update(project)
        return
