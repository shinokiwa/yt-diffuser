from typing import List
from injector import inject

from yt_diffuser.types.project import Project, ProjectLayer
from yt_diffuser.adapters.project.interface import IProjectRepository, IProjectRootRepository

class ProjectUseCase:
    """
    プロジェクトに関するユースケース
    """

    @inject
    def __init__(self, project_repository: IProjectRepository, project_root_repository: IProjectRootRepository):
        self.project_repository = project_repository
        self.root_repository = project_root_repository

    def is_exists(self, name: str) -> bool:
        """
        プロジェクトが存在するか確認する
        """
        return self.project_repository.is_exists(name)

    def create_project(self, project_name: str, width: int, height: int) -> None:
        """
        プロジェクトを作成する
        """
        project = Project(project_name=project_name, width=width, height=height)
        if self.is_exists(project_name):
            raise Exception(f"Project {project_name} already exists.")
        
        self.project_repository.save(project)
        return
     
    def get_project_list(self) -> List[Project]:
        """
        プロジェクトのリストを取得する
        """
        return self.root_repository.get_list()

    def get_project(self, name: str) -> Project:
        """
        プロジェクトを取得する
        """
        return self.project_repository.load(name)
    
    def remove_project(self, name: str) -> None:
        """
        プロジェクトを削除する
        """
        self.project_repository.remove(name)
        return
