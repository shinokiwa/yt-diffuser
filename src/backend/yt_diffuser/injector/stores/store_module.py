from injector import Binder, Module

from yt_diffuser.stores.database.store import IDBStore, DBStore
from yt_diffuser.stores.database.connection import IDBConnection, DBConnection

from yt_diffuser.stores.event.listener_store import IEventListnerStore, EventListenerStore

from yt_diffuser.stores.pipeline.pipeline_store import PipelineStore, IPipelineStore

from yt_diffuser.stores.process.process_context_store import IProcessContextStore, ProcessContextStore
from yt_diffuser.stores.process.process_store import IProcessStore, ProcessStore
from yt_diffuser.stores.process.process_queue_store import IProcessQueueStore, ProcessQueueStore

from yt_diffuser.stores.thread.thread_store import IThreadStore, ThreadStore

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
        binder.bind(IDBConnection, to=DBConnection)

        binder.bind(IPipelineStore, to=PipelineStore)

        binder.bind(IProcessContextStore, to=ProcessContextStore)
        binder.bind(IProcessQueueStore, to=ProcessQueueStore)
        binder.bind(IProcessStore, to=ProcessStore)

        binder.bind(IThreadStore, to=ThreadStore)