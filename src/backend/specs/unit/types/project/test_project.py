import pytest

from yt_diffuser.types.project.project import Project

class TestProject:
    """
    Projectクラスのテスト
    """

    def test_init(self):
        """
        __init__メソッドのテスト
        """
        project = Project(project_name="test", height=100, width=100)
        assert project.project_name == "test"
        assert project.height == 100
        assert project.width == 100
        assert project.version == 1
        assert project.layers.layers == {}
        assert project.layers.order == []
