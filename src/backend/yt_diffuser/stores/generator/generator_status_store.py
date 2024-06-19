from .interface import IGeneratorStatusStore, GeneratorStatusState

class GeneratorStatusStore(IGeneratorStatusStore):
    """
    生成処理プロセスの状態を管理するストア
    """

    _state = GeneratorStatusState()

    @property
    def state(self) -> GeneratorStatusState:
        return self.__class__._state
    
    def add_generate_total(self, count:int):
        self.__class__._state.generate_total += count
    
    def add_generate_count(self, count:int):
        self.__class__._state.generate_count += count
    
    def reset_count(self):
        self.__class__._state.generate_total = 0
        self.__class__._state.generate_count = 0