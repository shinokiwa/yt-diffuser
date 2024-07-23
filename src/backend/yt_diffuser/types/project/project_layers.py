from typing import Dict, List

from pydantic import BaseModel

from .project_layer import ProjectLayer

class ProjectLayers(BaseModel):
    """
    プロジェクトのレイヤー情報を保持するクラス
    """

    layers: Dict[str, ProjectLayer] = {}
    """
    レイヤー情報

    key: レイヤーID
    value: レイヤー情報
    """

    order: List[str] = []
    """
    レイヤーの描画順

    value: レイヤーID
    """

    def add_layer(self, layer: ProjectLayer):
        """
        レイヤーを先頭に追加する。
        """
        self.layers[str(layer.layer_id)] = layer
        self.order.insert(0, str(layer.layer_id))
    
    def is_exists(self, layer_id: str) -> bool:
        """
        指定したレイヤーIDが存在するか確認する。

        Args:
            layer_id (str): レイヤーID
        """
        return str(layer_id) in self.layers
    
    def remove_layer(self, layer_id: str):
        """
        レイヤーを削除する。

        Args:
            layer_id (str): レイヤーID
        """
        self.layers.pop(str(layer_id))
        self.order.remove(str(layer_id))
