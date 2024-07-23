from typing import List, Dict
from injector import inject

from yt_diffuser.types.path import AppPath

from .interface import IProjectRootRepository, IProjectRepository

class ProjectRootRepository(IProjectRootRepository):
    """
    プロジェクトのルートディレクトリを取得する
    """

    @inject
    def __init__(self, app_path: AppPath, project_repository: IProjectRepository):
        self.app_path = app_path
        self.project_repository = project_repository

    def get_list(self) -> List[Dict]:
        """
        プロジェクトのリストを取得する
        """
        path = self.app_path.OUTPUT_PROJECT_DIR
        projects = []
        if path.exists():
            for p in path.iterdir():
                project = self.project_repository.load(p.name)
                if project:
                    projects.append(project)
        
        return projects