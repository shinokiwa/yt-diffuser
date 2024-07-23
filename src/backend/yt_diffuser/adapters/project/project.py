from pathlib import Path
import shutil
import json

from injector import inject

from yt_diffuser.types.path import AppPath
from yt_diffuser.types.project import Project, ProjectLayer
from .interface import IProjectRepository

class ProjectRepository(IProjectRepository):
    """
    プロジェクトの本体ディレクトリを管理するアダプター
    """

    @inject
    def __init__(self, app_path: AppPath):
        self.app_path = app_path

    def get_path(self, name:str) -> Path:
        """
        プロジェクトのパスを取得する。

        Args:
            name (str): プロジェクト名
        """
        return self.app_path.OUTPUT_PROJECT_DIR / name
    
    def is_exists(self, name:str) -> bool:
        """
        プロジェクトが存在するか確認する。
        ディレクトリのみで判定し、index.jsonの有無は判断しない。

        Args:
            name (str): プロジェクト名
        """
        path = self.get_path(name)
        return path.is_dir()

    def save(self, project:Project) -> None:
        """
        プロジェクトを保存する

        Args:
            project (Project): 作成するプロジェクト
        """
        path = self.get_path(project.project_name)
        path.mkdir(parents=True, exist_ok=True)

        with open(path / "index.json", "w") as f:
            f.write(project.model_dump_json())
        return
    
    def load(self, name:str) -> Project:
        """
        プロジェクトを読み込む。

        it:
            - 対象が存在しない場合は例外を発生させる。
            - index.jsonが存在しない場合は、名称のみ設定された初期値のプロジェクトを返す。

        Args:
            name (str): プロジェクト名
        """
        if not self.is_exists(name):
            raise Exception(f"Project {name} does not exists.")

        path = self.get_path(name)

        if (path / "index.json").exists():
            with open(path / "index.json", "r") as f:
                return Project(**json.load(f))
        else:
            project = Project(project_name=name)
            return project
    
    def remove(self, name:str) -> None:
        """
        プロジェクトを削除する
        """
        if not self.is_exists(name):
            raise Exception(f"Project {name} does not exists.")

        path = self.get_path(name)
        shutil.rmtree(path, ignore_errors=True)
        return
    