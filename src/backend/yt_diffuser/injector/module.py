import logging; logger = logging.getLogger(__name__)

from injector import Binder, Module

from .stores.store_module import StoreInjectModule
from .adapters.adapter_module import AdapterInjectModule

class AppInjectModule(Module):
    """
    依存性注入を行うモジュール
    """

    def configure(self, binder:Binder):
        """
        バインディングを設定する
        """

        binder.install(StoreInjectModule)
        binder.install(AdapterInjectModule)