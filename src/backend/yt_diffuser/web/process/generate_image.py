"""
画像生成プロセスの制御モジュール

生成プロセスはシングルトンであり、
どこからアクセスしても同じプロセスを参照することができる。
また、生成プロセスは１つしか実行されない。

"""
import atexit
import multiprocessing
from multiprocessing.context import SpawnProcess
from logging import getLogger; logger = getLogger(__name__)

from yt_diffuser.config import AppConfig
from yt_diffuser.web.process.exceptions import DuplicateProcessError
from yt_diffuser.web.message_listener import get_context, get_message_queue
from yt_diffuser.workers.generate_image.generator import procedure

_process: SpawnProcess = None
_input_queue: multiprocessing.Queue = None


def is_running() -> bool:
    """
    ダウンロードプロセスが実行中かどうかを返す。

    ダウンロードプロセスが実行中の場合は実行命令は受け付けない。

    Returns:
        bool: ダウンロードプロセスが実行中の場合はTrue
    """
    return _process is not None and _process.is_alive()


def load(config:AppConfig, model_name:str, revision:str) -> SpawnProcess:
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
        args=(config, model_name, revision, message_queue, _input_queue),
        daemon=True
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


def generate_image(text:str) -> None:
    """
    画像生成プロセスに画像生成メッセージを送信する。

    Args:
        text (str): テキスト
    """
    input_message("generate-image", {"text": text})


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
        _process.join()
        _process = None

atexit.register(terminate)
