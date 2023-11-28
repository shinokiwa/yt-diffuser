""" ワーカーの処理を振り分ける

一部の処理については、実行可能かどうかに条件がある。
"""
from logging import getLogger; logger = getLogger(__name__)

from yt_diffuser.config import AppConfig
from yt_diffuser.worker.web_sender import get_send_queue
from yt_diffuser.worker.util.task import is_empty, is_running, run_task, stop_task 

import asyncio

worker_loop = None
worker_queue = asyncio.Queue()

def get_worker_queue (): return worker_queue
def get_worker_loop (): return worker_loop

async def loop (config:AppConfig):
    while True:
        (event, data) = await worker_queue.get()

        logger.debug('dispatch: event=%s', event)

        if event == "download":
            if is_empty() and not is_running():
                run_task(test_task, (config, event, data))

        elif event == "stop":
            if is_running():
                stop_task()
            else:
                logger.debug('task is not running')

        elif event == "load":
            pass
        elif event == "generate":
            pass

def start_worker (config:AppConfig):
    global worker_loop
    worker_loop = asyncio.new_event_loop()
    worker_loop.run_until_complete(loop(config))


async def test_task (config, event, data):
    logger.debug('test_task')
    from yt_diffuser.worker.util.tqdm import WorkerProgress
    progress = WorkerProgress(total=100)
    queue = get_send_queue()
    queue.put(('status', 'download-progress'))
    for i in range(10):
        await asyncio.sleep(1)
        progress.update(10)
    queue.put(('status', 'download-complete'))
