import pytest
import uuid
import json

from yt_diffuser.types.project.project_layer import ProjectLayer

class TestProjectLayer:
    """
    ProjectLayerクラスのテスト
    """

    def test_init(self):
        """
        __init__メソッドのテスト
        """
        project = ProjectLayer(layer_name="test")

        assert project.layer_name == "test"
        assert isinstance(project.layer_id, uuid.UUID)
        assert project.model_dump_json() == '{"layer_id":"'+ str(project.layer_id) + '","layer_name":"test","image":null,"i2i":null,"mask":null}'

