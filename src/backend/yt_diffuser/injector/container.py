from injector import Injector

from .module import AppInjectModule

container = None

def get_container() -> Injector:
    """
    コンテナを取得する。
    """
    global container

    if container is None:
        container = Injector([AppInjectModule()])

    return container

def get_depends(cls):
    """
    Dependsを取得する

    FastAPIのDepends用
    """
    return lambda: get_container().get(cls)