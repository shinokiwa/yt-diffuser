#!/bin/bash

NPM_HASH_FILE=/.npm_hash
PIP_HASH_FILE=/.pip_hash
PIP_DEV_HASH_FILE=/.pip_dev_hash

# 各ハッシュファイルをチェックし、異なる場合はパッケージをインストール

# npm install
if [ -f $NPM_HASH_FILE ]; then
    if [ "$(cat $NPM_HASH_FILE)" != "$(md5sum /workspace/src/frontend/package.json)" ]; then
        echo "package.jsonが変更されています。npm installを実行します。"
        cd /workspace/src/frontend
        /usr/bin/npm install
        md5sum /workspace/src/frontend/package.json > $NPM_HASH_FILE
    fi
else
    echo "package.jsonが存在しません。npm installを実行します。"
    cd /workspace/src/frontend
    /usr/bin/npm install
    md5sum /workspace/src/frontend/package.json > $NPM_HASH_FILE
fi

# pip install
if [ -f $PIP_HASH_FILE ]; then
    if [ "$(cat $PIP_HASH_FILE)" != "$(md5sum /workspace/src/backend/requirements.txt)" ]; then
        echo "requirements.txtが変更されています。pip installを実行します。"
        cd /workspace/src/backend
        /usr/bin/pip install -r requirements.txt
        md5sum /workspace/src/backend/requirements.txt > $PIP_HASH_FILE
    fi
else
    echo "requirements.txtが存在しません。pip installを実行します。"
    cd /workspace/src/backend
    /usr/bin/pip install -r requirements.txt
    md5sum /workspace/src/backend/requirements.txt > $PIP_HASH_FILE
fi

# pip install -r requirements-dev.txt
if [ -f $PIP_DEV_HASH_FILE ]; then
    if [ "$(cat $PIP_DEV_HASH_FILE)" != "$(md5sum /workspace/src/backend/requirements-dev.txt)" ]; then
        echo "requirements-dev.txtが変更されています。pip installを実行します。"
        cd /workspace/src/backend
        /usr/bin/pip install -r requirements-dev.txt
        md5sum /workspace/src/backend/requirements-dev.txt > $PIP_DEV_HASH_FILE
    fi
else
    echo "requirements-dev.txtが存在しません。pip installを実行します。"
    cd /workspace/src/backend
    /usr/bin/pip install -r requirements-dev.txt
    md5sum /workspace/src/backend/requirements-dev.txt > $PIP_DEV_HASH_FILE
fi

# バックグラウンドサーバー起動
cd /workspace/src/backend
/usr/bin/python3 -m yt_diffuser 2>&1 &

# フロントエンドサーバー起動
cd /workspace/src/frontend
/usr/bin/npm run dev 2>&1 &

# Nginx起動
/usr/sbin/nginx -g 'daemon off;'
