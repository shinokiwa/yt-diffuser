#!/bin/bash

NPM_HASH_FILE=/.npm_hash
PIP_TORCH_HASH_FILE=/.pip_torch_hash
PIP_HASH_FILE=/.pip_hash
PIP_DEV_HASH_FILE=/.pip_dev_hash

FRONTEND_DIR=/workspace/src/frontend
BACKEND_DIR=/workspace/src/backend

# 各ハッシュファイルをチェックし、異なる場合はパッケージをインストール
# ハッシュファイルが存在しない場合は処理しない

# npm install
if [ -e $FRONTEND_DIR/package.json ]; then
  if [ -f $NPM_HASH_FILE ]; then
    if [ "$(cat $NPM_HASH_FILE)" != "$(md5sum $FRONTEND_DIR/package.json)" ]; then
      echo "package.jsonが変更されています。npm installを実行します。"
      cd $FRONTEND_DIR
      /usr/bin/npm install
      md5sum $FRONTEND_DIR/package.json > $NPM_HASH_FILE
    fi
  else
    echo "以前のインストールが見つかりません。npm installを実行します。"
    cd $FRONTEND_DIR
    /usr/bin/npm install
    md5sum $FRONTEND_DIR/package.json > $NPM_HASH_FILE
  fi
else
  echo "package.jsonが見つかりません。"
fi

# pip install -r requirements-torch.txt
if [ -e $BACKEND_DIR/requirements-torch.txt ]; then
  if [ -f $PIP_TORCH_HASH_FILE ]; then
    if [ "$(cat $PIP_TORCH_HASH_FILE)" != "$(md5sum $BACKEND_DIR/requirements-torch.txt)" ]; then
      echo "requirements-torch.txtが変更されています。pip installを実行します。"
      cd $BACKEND_DIR
      /usr/bin/pip install -r requirements-torch.txt
      md5sum $BACKEND_DIR/requirements-torch.txt > $PIP_TORCH_HASH_FILE
    fi
  else
    echo "requirements-torch.txtが存在しません。pip installを実行します。"
    cd $BACKEND_DIR
    /usr/bin/pip install -r requirements-torch.txt
    md5sum $BACKEND_DIR/requirements-torch.txt > $PIP_TORCH_HASH_FILE
  fi
else
  echo "requirements-torch.txtが見つかりません。"
fi

# pip install
if [ -e $BACKEND_DIR/requirements.txt ]; then
  if [ -f $PIP_HASH_FILE ]; then
    if [ "$(cat $PIP_HASH_FILE)" != "$(md5sum $BACKEND_DIR/requirements.txt)" ]; then
      echo "requirements.txtが変更されています。pip installを実行します。"
      cd $BACKEND_DIR
      /usr/bin/pip install -r requirements.txt
      md5sum $BACKEND_DIR/requirements.txt > $PIP_HASH_FILE
    fi
  else
    echo "requirements.txtが存在しません。pip installを実行します。"
    cd $BACKEND_DIR
    /usr/bin/pip install -r requirements.txt
    md5sum $BACKEND_DIR/requirements.txt > $PIP_HASH_FILE
  fi
else
  echo "requirements.txtが見つかりません。"
fi


# pip install -r requirements-dev.txt
if [ -e $BACKEND_DIR/requirements-dev.txt ]; then
  if [ -f $PIP_DEV_HASH_FILE ]; then
    if [ "$(cat $PIP_DEV_HASH_FILE)" != "$(md5sum $BACKEND_DIR/requirements-dev.txt)" ]; then
      echo "requirements-dev.txtが変更されています。pip installを実行します。"
      cd $BACKEND_DIR
      /usr/bin/pip install -r requirements-dev.txt
      md5sum $BACKEND_DIR/requirements-dev.txt > $PIP_DEV_HASH_FILE
    fi
  else
    echo "requirements-dev.txtが存在しません。pip installを実行します。"
    cd $BACKEND_DIR
    /usr/bin/pip install -r requirements-dev.txt
    md5sum $BACKEND_DIR/requirements-dev.txt > $PIP_DEV_HASH_FILE
  fi
else
  echo "requirements-dev.txtが見つかりません。"
fi

# バックエンドサーバー起動
cd $BACKEND_DIR
/usr/bin/python3 -m yt_diffuser 2>&1 &

# フロントエンドサーバー起動
cd $FRONTEND_DIR
/usr/bin/npm run dev 2>&1 &

# Nginx起動
/usr/sbin/nginx -g 'daemon off;'
