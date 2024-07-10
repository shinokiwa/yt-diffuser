from abc import ABCMeta, abstractmethod
from typing import List
from pathlib import Path

from yt_diffuser.types.project import Project

class IProjectDirectoryAdapter(metaclass=ABCMeta):
    """
    プロジェクトディレクトリアダプタのインターフェース
    """

    @abstractmethod
    def get_path(self, name:str) -> Path:
        """
        プロジェクトのパスを取得する
        """
        pass

    @abstractmethod
    def is_exists(self, name:str) -> bool:
        """
        プロジェクトが存在するか確認する
        """
        pass

    @abstractmethod
    def create(self, project:Project) -> None:
        """
        プロジェクトを新規作成する

        Args:
            project (Project): 作成するプロジェクト
        """
        pass

    @abstractmethod
    def update(self, project:Project) -> None:
        """
        プロジェクトを更新する

        Args:
            project (Project): 更新するプロジェクト
        """
        pass

    @abstractmethod
    def get_project(self, name:str) -> Project:
        """
        プロジェクトを取得する
        """
        pass

    @abstractmethod
    def remove(self, name:str) -> None:
        """
        プロジェクトを削除する
        """
        pass

    @abstractmethod
    def get_list(self) -> List[Project]:
        """
        プロジェクトのリストを取得する
        """
        pass

    @abstractmethod
    def get_layer_path(self, project_name:str, layer_name:str) -> Path:
        """
        レイヤーのパスを取得する
        """
        pass

    @abstractmethod
    def add_layer(self, project_name:str, layer_name:str) -> None:
        """
        レイヤーを新規作成する
        """
        pass

