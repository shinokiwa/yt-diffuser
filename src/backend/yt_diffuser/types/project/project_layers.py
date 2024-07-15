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
        レイヤーを追加する。
        """
        self.layers[str(layer.layer_id)] = layer
        self.order.append(str(layer.layer_id))
    
    def is_exists(self, layer_id: str) -> bool:
        """
        指定したレイヤーIDが存在するか確認する。

        Args:
            layer_id (str): レイヤーID
        """
        return str(layer_id) in self.layers
