from abc import ABCMeta, abstractmethod

from pydantic import BaseModel

class GeneratorStatusState(BaseModel):
    base_model_id:str = ""
    generate_total:int = 0
    generate_count:int = 0
    stop_signal:bool = False
    exit_signal:bool = False

class IGeneratorStatusStore(metaclass=ABCMeta):
    """
    生成処理プロセスの状態を管理するストアインターフェース
    """

    @abstractmethod
    def state(self) -> GeneratorStatusState:
        """
        状態の取得
        """
        pass

    @abstractmethod
    def add_generate_total(self, count:int):
        """
        生成合計数の追加
        """
        pass

    @abstractmethod
    def add_generate_count(self, count:int):
        """
        生成カウント数の追加
        """
        pass

    @abstractmethod
    def reset_count(self):
        """
        生成合計数、生成カウント数のリセット
        """
        pass
