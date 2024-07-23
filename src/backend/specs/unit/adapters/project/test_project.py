import pytest
import shutil
from pathlib import Path
import json

from specs.unit.injector import get_container

from yt_diffuser.types.project import Project
from yt_diffuser.adapters.project.project import AppPath, ProjectRepository

class TestProjectRepository:
    """
    ProjectRepository

    it:
        - プロジェクトの本体ディレクトリを管理するアダプター
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
        app_path:AppPath = container.get(AppPath)
        app_path.OUTPUT_PROJECT_DIR.mkdir(parents=True, exist_ok=True)
        yield
        shutil.rmtree(app_path.OUTPUT_PROJECT_DIR)

    def test_get_path(self, container):
        """
        get_path

        it:
            - プロジェクトのパスを取得する。
        """
        adapter = container.get(ProjectRepository)
        path = adapter.get_path("test")
        assert path.name == "test"

    def test_is_exists(self, container):
        """
        is_exists

        it:
            - プロジェクトが存在するか確認する。
        """
        adapter = container.get(ProjectRepository)

        assert adapter.is_exists("test") == False

        path = adapter.app_path.OUTPUT_PROJECT_DIR / "test"
        path.mkdir(parents=True, exist_ok=True)
        assert adapter.is_exists("test") == True


    def test_save(self, container):
        """
        save

        it:
            - プロジェクトを保存する。
        """
        adapter = container.get(ProjectRepository)

        assert adapter.is_exists("test") == False

        path:Path = adapter.app_path.OUTPUT_PROJECT_DIR / "test"
        project = Project(project_name="test", width=100, height=100)
        adapter.save(project)
        assert path.exists() == True

        with open(path / "index.json", "r") as f:
            data = f.read()
            json_data = json.loads(data)

        assert json_data == {
            "project_name": "test",
            "width": 100,
            "height": 100,
            "layers": {
                "layers": {},
                "order": []
            },
            "version": 1
        }

    def test_load(self, container):
        """
        load

        it:
            - プロジェクトを読み込む。
            - 対象が存在しない場合は例外を発生させる。
            - index.jsonが存在しない場合は、名称のみ設定された初期値のプロジェクトを返す。
        """
        adapter = container.get(ProjectRepository)

        new_project = Project(project_name="test", width=100, height=100)
        adapter.save(new_project)

        project1 = adapter.load("test")
        assert project1.project_name == "test"
        assert project1.width == 100
        assert project1.height == 100    

        (adapter.app_path.OUTPUT_PROJECT_DIR / "test2").mkdir(parents=True, exist_ok=True)
        project2 = adapter.load("test2")
        def_project = Project(project_name="test2")
        assert project2.project_name == "test2"
        assert project2.width == def_project.width
        assert project2.height == def_project.height

        with pytest.raises(Exception):
            project3 = adapter.load("test3")

    def test_remove(self, container):
        """
        remove

        it:
            - プロジェクトを削除する。
        """
        adapter = container.get(ProjectRepository)

        project = Project(project_name="test", width=100, height=100)
        adapter.save(project)
        assert adapter.is_exists("test") == True

        adapter.remove("test")
        assert adapter.is_exists("test") == False
    
