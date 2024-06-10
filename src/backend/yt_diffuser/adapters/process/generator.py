import atexit
import multiprocessing
from multiprocessing.context import SpawnProcess
from logging import getLogger; logger = getLogger(__name__)

from injector import inject

from yt_diffuser.config import AppConfig
from yt_diffuser.types import ProcessKey, DuplicateProcessError
from yt_diffuser.stores.process.process import ProcessStore, ProcessData

from yt_diffuser.utils.event.process import get_context, get_message_queue
from yt_diffuser.workers.generate_image.main import procedure


class GeneratorProcess:
    """
    生成プロセスへのアダプター
    """

    @inject
    def __init__(self, config:AppConfig, store:ProcessStore):
        self.config = config
        self.store = store
        self.key = ProcessKey.GENERATOR
    
    def is_running(self) -> bool:
        """
        生成プロセスが動作中かどうかを返す。
        生成プロセスはダウンロードプロセスと違い、実行中しか命令を受け付けない。

        Returns:
            bool: ダウンロードプロセスが実行中の場合はTrue
        """
        process = self.store.get_process(self.key)
        return process is not None and process.process.is_alive()


def load(config:AppConfig, model_name:str, revision:str, compile:bool) -> SpawnProcess:
    """
    画像生成プロセスを実行する。
    この段階ではモデルを読み込むだけ。

    画像生成プロセスは１つしか実行されない。

    Args:
        repo_id (str): リポジトリID
        revision (str): リビジョン
    
    Returns:
        multiprocessing.context.SpawnProcess: ダウンロードプロセス
    
    Raises:
        DuplicateProcessError: ダウンロードプロセスが実行中の場合
    """
    global _process, _input_queue

    if is_running():
        raise DuplicateProcessError("download process is already running")
    
    context = get_context()
    message_queue = get_message_queue()
    _input_queue = context.Queue()

    logger.debug(f"generate_image call: {model_name}:{revision}")
    _process = context.Process(
        target=procedure,
        args=(config, model_name, revision, compile, message_queue, _input_queue),
        #daemon=True
    )

    _process.start()

    return _process


def input_message(message:str, data:dict=None) -> None:
    """
    画像生成プロセスにメッセージを送信する。

    Args:
        message (str): メッセージ
        data (dict): 付随データ
    """
    global _input_queue

    if not is_running() or _input_queue is None:
        raise RuntimeError("generate image process is not running")

    _input_queue.put((message, data))


def text_to_image(data:dict) -> None:
    """
    画像生成プロセスに画像生成メッセージを送信する。

    Args:
        data (dict): t2iデータ
    """
    input_message("text-to-image", data)

def image_to_image(data:dict) -> None:
    """
    画像生成プロセスに画像生成メッセージを送信する。

    Args:
        data (dict): i2iデータ
    """
    input_message("image-to-image", data)

def inpaint(data:dict) -> None:
    """
    画像生成プロセスに画像生成メッセージを送信する。

    Args:
        data (dict): inpaintデータ
    """
    input_message("inpaint", data)

def compile() -> None:
    """
    画像生成プロセスにコンパイルメッセージを送信する。
    """
    input_message("compile", {})


def remove_lora() -> None:
    """
    画像生成プロセスにLORA解放メッセージを送信する。
    """
    input_message("remove-lora")


def terminate() -> None:
    """
    画像生成プロセスを終了する。

    停止状態のプロセスを終了してもエラーにならない。
    現在は強制的に終了させている。
    ワーカー側は強制終了の可能性を考慮しておく必要がある。
    """
    global _process

    if is_running():
        logger.debug("Terminate generate_image")
        input_message("exit")
        _process.join(timeout=30)
        if _process.is_alive():
            logger.debug("Force terminate generate_image")
            _process.terminate()
        _process = None

atexit.register(terminate)
