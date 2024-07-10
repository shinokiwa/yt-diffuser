from injector import Binder, Module

from yt_diffuser.adapters.generator.controller import GeneratorController, IGeneratorController
from yt_diffuser.adapters.generator.generator import Generator, IGenerator
from yt_diffuser.adapters.generator.presenter import GeneratorPresenter, IGeneratorPresenter
from yt_diffuser.adapters.project.project_directory import ProjectDirectoryAdapter, IProjectDirectoryAdapter

class AdapterInjectModule(Module):
    """
    依存性注入を行うモジュール
    """

    def configure(self, binder:Binder):
        binder.bind(IGeneratorController, to=GeneratorController)
        binder.bind(IGenerator, to=Generator)
        binder.bind(IGeneratorPresenter, to=GeneratorPresenter)

        binder.bind(IProjectDirectoryAdapter, to=ProjectDirectoryAdapter)