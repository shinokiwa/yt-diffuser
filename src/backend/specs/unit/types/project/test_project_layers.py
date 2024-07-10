import pytest

from yt_diffuser.types.project.project_layers import ProjectLayers

class TestProjectLayers:
    """
    ProjectLayersクラスのテスト
    """

    def test_init(self):
        """
        __init__メソッドのテスト
        """
        project = ProjectLayers()

        assert project.layers == {}
        assert project.order == []
