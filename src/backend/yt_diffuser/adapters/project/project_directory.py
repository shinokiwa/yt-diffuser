from typing import List
from pathlib import Path
import shutil
import json

from injector import inject

from yt_diffuser.types.path import AppPath
from yt_diffuser.types.project import Project

from .interface import IProjectDirectoryAdapter

class ProjectDirectoryAdapter(IProjectDirectoryAdapter):
    """
    プロジェクトのディレクトリやファイルを管理するアダプター
    """

    @inject
    def __init__(self, app_path: AppPath):
        self.app_path = app_path

    def get_path(self, name:str) -> Path:
        """
        プロジェクトのパスを取得する
        """
        return self.app_path.OUTPUT_PROJECT_DIR / name
    
    def is_exists(self, name:str) -> bool:
        """
        プロジェクトが存在するか確認する
        """
        return self.get_path(name).exists()

    def create(self, project:Project) -> None:
        """
        プロジェクトを新規作成する

        Args:
            project (Project): 作成するプロジェクト
        """
        path = self.get_path(project.project_name)
        path.mkdir(parents=True, exist_ok=True)

        with open(path / "index.json", "w") as f:
            f.write(project.model_dump_json())
        return
    
    def update(self, project:Project) -> None:
        """
        プロジェクトを更新する

        Args:
            project (Project): 更新するプロジェクト
        """
        path = self.get_path(project.project_name)
        if not path.is_dir():
            return
        
        with open(path / "index.json", "w") as f:
            f.write(project.model_dump_json())
        return
    
    def get_project(self, name:str) -> Project:
        """
        プロジェクトを取得する
        """
        path = self.get_path(name)
        if not path.is_dir() or not (path / "index.json").exists():
            return None
    
        with open(path / "index.json", "r") as f:
            project = Project(**json.load(f))
        return project
    
    def remove(self, name:str) -> None:
        """
        プロジェクトを削除する
        """
        path = self.get_path(name)
        shutil.rmtree(path, ignore_errors=True)
        return
    
    def get_list(self) -> List[Project]:
        """
        プロジェクトのリストを取得する
        """
        path = self.app_path.OUTPUT_PROJECT_DIR
        projects = []
        if path.exists():
            for p in path.iterdir():
                project = self.get_project(p.name)
                if project:
                    projects.append(project)
        
        return projects

    
    def get_layer_path(self, project_name:str, layer_id:str) -> Path:
        """
        レイヤーのパスを取得する
        """
        return self.get_path(project_name) / "layers" / layer_id
    
    def add_layer(self, project_name:str, layer_id:str) -> None:
        """
        レイヤーディレクトリを追加する
        """
        if not self.is_exists(project_name):
            return

        path = self.get_layer_path(project_name, layer_id)
        path.mkdir(parents=True, exist_ok=True)
        return