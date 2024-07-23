import pytest
import shutil

from specs.unit.injector import get_container

from yt_diffuser.types.project import Project
from yt_diffuser.adapters.project.project_directory import ProjectDirectoryAdapter

class TestProjectDirectory:
    """
    ProjectDirectoryAdapter

    プロジェクトディレクトリのアダプター
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
        adapter:ProjectDirectoryAdapter = container.get(ProjectDirectoryAdapter)
        adapter.app_path.OUTPUT_PROJECT_DIR.mkdir(parents=True, exist_ok=True)
        yield
        shutil.rmtree(adapter.app_path.OUTPUT_PROJECT_DIR)

    def test_get_path(self, container):
        """
        get_path

        it:
            - プロジェクトのパスを取得する。
        """
        adapter = container.get(ProjectDirectoryAdapter)
        path = adapter.get_path("test")
        assert path.name == "test"

    def test_is_exists(self, container):
        """
        is_exists

        it:
            - プロジェクトが存在するか確認する。
        """
        adapter = container.get(ProjectDirectoryAdapter)
        assert adapter.is_exists("test") == False

    def test_create(self, container):
        """
        
        """
        adapter = container.get(ProjectDirectoryAdapter)

        assert adapter.is_exists("test") == False

        project = Project(project_name="test", width=100, height=100)
        adapter.create(project)
        assert adapter.is_exists("test") == True

    def test_get_project(self, container):
        """
        get_project

        it:
            - プロジェクトを取得する。
        """
        adapter = container.get(ProjectDirectoryAdapter)

        project1 = Project(project_name="test", width=100, height=100)
        adapter.create(project1)

        project2 = adapter.get_project("test")
        assert project2.project_name == "test"
        assert project2.width == 100
        assert project2.height == 100    

    def test_remove(self, container):
        """
        remove

        it:
            - プロジェクトを削除する。
        """
        adapter = container.get(ProjectDirectoryAdapter)

        project = Project(project_name="test", width=100, height=100)
        adapter.create(project)
        assert adapter.is_exists("test") == True

        adapter.remove("test")
        assert adapter.is_exists("test") == False
    
    def test_get_list(self, container):
        """
        get_list

        it:
            - プロジェクトのリストを取得する。
        """
        adapter = container.get(ProjectDirectoryAdapter)
        projects = adapter.get_list()
        assert projects == []

        project = Project(project_name="test", width=100, height=100)
        adapter.create(project)
        projects = adapter.get_list()
        assert len(projects) > 0
        assert projects[0].project_name == "test"
    
    def test_update(self, container):
        """
        update

        it:
            - プロジェクトを更新する。
        """
        adapter = container.get(ProjectDirectoryAdapter)

        project = Project(project_name="test", width=100, height=100)
        adapter.create(project)
        project.width = 200
        adapter.update(project)

        project = adapter.get_project("test")
        assert project.width == 200