from typing import Union
from pathlib import Path
import shutil
import uuid

from injector import inject

from yt_diffuser.types.path import AppPath
from yt_diffuser.types.project import Project, ProjectLayer

from .interface import IProjectLayerRepository, IProjectRepository

class ProjectLayerRepository(IProjectLayerRepository):
    """
    プロジェクトのレイヤーを管理するアダプター
    """

    @inject
    def __init__(self, app_path: AppPath, project_repository:IProjectRepository):
        self.app_path = app_path
        self.project_repository = project_repository
    
    def get_path(self, project_name:str, layer_id:str) -> Path:
        """
        レイヤーのパスを取得する
        """
        return self.project_repository.get_path(project_name) / "layers" / layer_id
    
    def is_exists(self, project_name:str, layer:ProjectLayer) -> bool:
        """
        レイヤーが存在するか確認する
        """
        return self.get_path(project_name, layer).exists()
    
    def create(self, project_name:str, layer:ProjectLayer) -> Project:
        """
        レイヤーディレクトリを作成する
        """
        if not self.project_repository.is_exists(project_name):
            raise Exception(f"Project {project_name} does not exists.")
        
        if self.is_exists(project_name, layer):
            raise Exception(f"Layer {layer.layer_id} already exists.")
        
        project = self.project_repository.load(project_name)

        path = self.get_path(project_name, layer)
        path.mkdir(parents=True, exist_ok=True)

        project.layers.add_layer(layer)
        self.project_repository.save(project)
        return project
    
    def save_image (self, project_name:str, layer_id:str, file_name:str, source_path:str, is_copy:bool = False) -> None:
        """
        画像を保存する
        実際には保存済みの画像を移動するだけ

        Args:
            project_name (str): プロジェクト
            layer_id (str): レイヤーID
            file_name (str): ファイル名
            source_path (str): 画像のソースパス
            is_copy (bool): コピーするかどうか Falseの場合は移動する (default: False)
        """
        project = self.project_repository.load(project_name)
        project.layers.layers[layer_id].image = file_name

        path = self.get_path(project_name, layer_id) / file_name
        if is_copy:
            shutil.copy(source_path, path)
        else:
            shutil.move(source_path, path)
        
        self.project_repository.save(project)

        return
    
    def remove(self, project_name:str, layer:ProjectLayer) -> None:
        """
        レイヤーディレクトリを削除する
        """
        path = self.get_path(project_name, layer)
        layer_id = str(layer.layer_id)
        shutil.rmtree(path, ignore_errors=True)

        project = self.project_repository.load(project_name)
        project.layers.remove_layer(layer_id)
        self.project_repository.save(project)
        return