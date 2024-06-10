"""
テスト用の依存性注入を行うモジュール
"""
from tempfile import TemporaryDirectory
from injector import Injector, Binder, Module, singleton

from fastapi import Depends

from yt_diffuser.injector.module import AppInjectModule
from yt_diffuser.config import AppConfig
from yt_diffuser.types.path import AppPath

class TestInjectModule(Module):
    """
    テスト用の依存性注入を行うモジュール
    """

    def configure(self, binder:Binder):
        """
        バインディングを設定する
        """
        binder.install(AppInjectModule)

        config = AppConfig()
        binder.bind(AppConfig, to=config)

        # :memory: を使いたいがwithを抜けるたびにデータが消えるので、テンポラリディレクトリを使う
        pathDef = AppPath(base_dir=TemporaryDirectory().name)
        binder.bind(AppPath, to=pathDef, scope=singleton)

container = None

def get_container():
    """
    コンテナを取得する。
    """
    global container

    if container is None:
        container = Injector([TestInjectModule()])

    return container
