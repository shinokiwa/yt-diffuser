from abc import ABCMeta, abstractmethod
from typing import List, Union
from pathlib import Path
import uuid

from yt_diffuser.types.project import Project, ProjectLayer

class IProjectRepository(metaclass=ABCMeta):
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
    def save(self, project:Project) -> None:
        """
        プロジェクトを保存する

        Args:
            project (Project): 作成するプロジェクト
        """
        pass
    
    @abstractmethod
    def load(self, name:str) -> Project:
        """
        プロジェクトを読み込む
        """
        pass

    @abstractmethod
    def remove(self, name:str) -> None:
        """
        プロジェクトを削除する
        """
        pass

class IProjectRootRepository(metaclass=ABCMeta):
    @abstractmethod
    def get_list(self) -> List[Project]:
        """
        プロジェクトのリストを取得する
        """
        pass

class IProjectLayerRepository(metaclass=ABCMeta):
    """
    プロジェクトレイヤーアダプタのインターフェース
    """

    @abstractmethod
    def get_path(self, project_name:str, layer_id:str) -> Path:
        """
        レイヤーのパスを取得する
        """
        pass

    @abstractmethod
    def is_exists(self, project_name:str, layer_id:str) -> bool:
        """
        レイヤーが存在するか確認する
        """
        pass

    @abstractmethod
    def create(self, project_name:str, layer:ProjectLayer) -> Project:
        """
        レイヤーディレクトリを作成する
        """
        pass

    @abstractmethod
    def save_image (self, project_name:str, layer_id:str, file_name:str, source_path:str, is_copy:bool = True) -> None:
        """
        画像を保存する
        """
        pass

    @abstractmethod
    def remove(self, project_name:str, layer:ProjectLayer) -> None:
        """
        レイヤーを削除する
        """
        pass