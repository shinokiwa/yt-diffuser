"""
メイン処理
"""
import os
import sys
import logging; logger = logging.getLogger('yt_diffuser')
logging.basicConfig(stream=sys.stdout)
import multiprocessing

from yt_diffuser.injector import get_container
from .controller import GeneratorController

def generator_main (send_queue:multiprocessing.Queue = None, recv_queue:multiprocessing.Queue = None):
    """
    生成処理のメイン処理
    """
    if os.environ.get('DEBUG') == '1':
        logger.setLevel(level=logging.DEBUG)

    logger.debug("generator_main start")

    controller = get_container().get(GeneratorController)
    controller.main_loop(recv_queue, send_queue)
