""" huggingface.py のテスト
"""
import pytest

from yt_diffuser.worker.download.huggingface import (
    model_download
)

def test_test():
    config_dict = model_download()

    print(f"config_dict: {config_dict}")


