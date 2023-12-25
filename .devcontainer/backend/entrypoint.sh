#!/bin/sh

# 環境変数 BACKEND_REBUILD が true の場合、pip install を実行する
if [ "$BACKEND_REBUILD" = "true" ]; then
  /usr/bin/python3 -m pip install --no-cache-dir --upgrade pip setuptools wheel
  /usr/bin/python3 -m pip install -r /workspace/src/backend/requirements.txt
fi

/usr/bin/python3 -m yt_diffuser