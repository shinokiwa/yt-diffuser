from injector import Binder, Module, singleton

from yt_diffuser.stores.database.store import IDBStore, DBStore
from yt_diffuser.stores.database.connection import IDBConnection, DBConnection

from yt_diffuser.stores.event.listener_store import IEventListnerStore, EventListenerStore

from yt_diffuser.stores.pipeline.pipeline_store import PipelineStore, IPipelineStore

from yt_diffuser.stores.process.process_context_store import IProcessContextStore, ProcessContextStore
from yt_diffuser.stores.process.process_store import IProcessStore, ProcessStore
from yt_diffuser.stores.process.process_queue_store import IProcessQueueStore, ProcessQueueStore

from yt_diffuser.stores.generator.generator_status_store import IGeneratorStatusStore, GeneratorStatusStore

class StoreInjectModule(Module):
    """
    依存性注入を行うモジュール
    """

    def configure(self, binder:Binder):
        """
        バインディングを設定する
        """
        binder.bind(IEventListnerStore, to=EventListenerStore)

        binder.bind(IDBStore, to=DBStore)
        binder.bind(IDBConnection, to=DBConnection, scope=singleton)

        binder.bind(IPipelineStore, to=PipelineStore)

        binder.bind(IProcessContextStore, to=ProcessContextStore)
        binder.bind(IProcessQueueStore, to=ProcessQueueStore)
        binder.bind(IProcessStore, to=ProcessStore)

        binder.bind(IGeneratorStatusStore, to=GeneratorStatusStore)
