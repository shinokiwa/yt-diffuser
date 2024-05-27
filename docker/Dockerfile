#################################
# ゆとりでふーざー構成用のDockerfile
#################################

#################################
# ベースイメージ
#################################
# NVIDIA CUDA 12.1 Ubuntu用をベースイメージにする
FROM nvidia/cuda:12.1.0-base-ubuntu22.04 AS base

# 必要なパッケージをインストール
RUN apt-get update && apt-get install -y --no-install-recommends \
    language-pack-ja \
    build-essential \
    curl \
    git \
    python3-pip python3-venv \
    python3.10-dev \
    libgl1-mesa-glx libglib2.0-0 \
    nginx \
    && rm -rf /var/lib/apt/lists/*

# PyTorchインストール
# 時間がかかるのでキャッシュ作成用に分ける
WORKDIR /workspace/src/backend/
RUN python3 -m pip install --no-cache-dir --upgrade pip setuptools wheel
COPY ./src/backend/requirements-torch.txt /workspace/src/backend/
RUN python3 -m pip install -r /workspace/src/backend/requirements-torch.txt

# Pythonセットアップ
COPY ./src/backend/ /workspace/src/backend/
RUN python3 -m pip install -r /workspace/src/backend/requirements.txt
RUN python3 -m pip install -r /workspace/src/backend/requirements-dev.txt

# ポート設定
EXPOSE 80

#################################
## DevServerステージ
## 開発用サーバーの場合はここで止める
#################################
FROM base AS devserver

# Node.jsインストール
RUN curl -sL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get update \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# npmインストール
WORKDIR /workspace/src/frontend
COPY ./src/frontend/ /workspace/src/frontend/
RUN npm install

# Nginxの設定
COPY ./docker/dev/etc/nginx/nginx.conf /etc/nginx/nginx.conf

# ワークスペースの設定
WORKDIR /workspace/src/

COPY ./docker/dev/entrypoint.sh /
RUN chmod +x /entrypoint.sh
ENTRYPOINT [ "/entrypoint.sh" ]

#################################
## Buildステージ
## フロントエンドのビルドを行う
#################################
FROM devserver AS build

WORKDIR /workspace/src/frontend
RUN npm run build

#################################
## Productionステージ
#################################
FROM base AS production

# Nginx設定ファイルをコピー
COPY ./docker/prod/etc/nginx/nginx.conf /etc/nginx/nginx.conf

# ビルド済みのフロントエンドをコピー
RUN mkdir -p /workspace/src/frontend/dist
COPY --from=build /workspace/src/frontend/dist /workspace/src/frontend/dist

# ENTRYPOINTを設定
COPY ./docker/prod/entrypoint.sh /
RUN chmod +x /entrypoint.sh
ENTRYPOINT [ "/entrypoint.sh" ]