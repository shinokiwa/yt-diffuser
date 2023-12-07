""" ダウンロードのプロシージャ
"""
import os
import sys
import asyncio
import shlex
from multiprocessing import Queue

from yt_diffuser.config import AppConfig
from yt_diffuser.worker.util.tqdm import WorkerProgress
from yt_diffuser.store import connect_database, HFModelStore

async def download_procedure(config:AppConfig, queue:Queue, event, data):
    """ ダウンロードのプロシージャ
    """
    repo_id = "CompVis/stable-diffusion-v1-4"
    revision = "fp16"

    queue.put(('message', f"download-start:{repo_id}/{revision}"))

    process = await asyncio.create_subprocess_exec(
        sys.executable,
        "yt_diffuser/store/hf_download.py",
        config.STORE_HF_MODEL_DIR,
        shlex.quote(repo_id),
        shlex.quote(revision),
        os.environ.get('TEST', '0'),
        cwd=os.getcwd(),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT
    )
    await asyncio.sleep(0)

    tqdm = WorkerProgress(queue=queue, status='download', target=f"{repo_id}/{revision}", miniters=0, mininterval=0)
    while True:
        if process.stdout.at_eof():
            break

        prev_progress = 0
        async for stdout in process.stdout:
            stdout = stdout.decode().strip()
            if stdout:
                (progress, total) = stdout.split('/')

                tqdm.total = int(total)
                progress = int(progress)
                tqdm.update(progress - prev_progress)
                prev_progress = progress

    await process.communicate()

    conn = connect_database(config.DB_FILE)
    hf_model_store = HFModelStore(conn, repo_id=repo_id, revision=revision)
    hf_model_store.save()
    conn.commit()

    queue.put(('message', f"download-complete:{repo_id}/{revision}"))
