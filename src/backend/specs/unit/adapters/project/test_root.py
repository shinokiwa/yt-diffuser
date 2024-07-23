import pytest
import shutil

from specs.unit.injector import get_container

from yt_diffuser.types.project import Project
from yt_diffuser.adapters.project.root import ProjectRootRepository

class TestProjectRootRepository:
    """
    ProjectRootRepository

    it:
        - プロジェクトのルートディレクトリを管理するアダプター
    """

    @pytest.fixture
    def container(self):
        return get_container()
    
    @pytest.fixture(autouse=True, scope="function")
    def setup(self, container):
        """
        前後処理
        プロジェクトディレクトリを初期化する。
        """
        adapter:ProjectRootRepository = container.get(ProjectRootRepository)
        adapter.app_path.OUTPUT_PROJECT_DIR.mkdir(parents=True, exist_ok=True)
        yield
        shutil.rmtree(adapter.app_path.OUTPUT_PROJECT_DIR)

    def test_get_list(self, container):
        """
        get_list

        it:
            - プロジェクトのリストを取得する。
        """
        adapter = container.get(ProjectRootRepository)
        projects = adapter.get_list()
        assert projects == []

        path = adapter.app_path.OUTPUT_PROJECT_DIR

        (path / "test").mkdir(parents=True, exist_ok=True)
        (path / "test2").mkdir(parents=True, exist_ok=True)

        projects = adapter.get_list()
        assert len(projects) == 2
        # 順序不定なのでソートする
        projects = sorted(projects, key=lambda x: x.project_name)
        assert projects[0].project_name == "test"
        assert projects[1].project_name == "test2"
    