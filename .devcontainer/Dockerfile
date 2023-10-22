# バックエンドコンテナと、マルチステージビルドでDevContainerのイメージを構成

# NVIDIA CUDA 11.7 Ubuntu用をベースイメージにする
FROM nvidia/cuda:11.7.1-base-ubuntu22.04 AS backend

# バックエンドコンテナに必要なパッケージをインストール
RUN apt-get update && apt-get install -y --no-install-recommends \
    language-pack-ja \
    build-essential \
    git curl \
    python3-pip python3-venv

# workspaceディレクトリを作成
WORKDIR /workspace/src/backend/

# pipインストール
COPY ./src/backend/requirements.txt /workspace/src/backend/
RUN python3 -m pip install --no-cache-dir --upgrade pip setuptools wheel
RUN python3 -m pip install -r /workspace/src/backend/requirements.txt

CMD ["python3", "-m", "yt_diffuser"]

#################################

# DevContainer用のイメージを構成
FROM backend AS devcontainer

WORKDIR /workspace/src/frontend

# Node.jsをインストール
RUN curl -sL https://deb.nodesource.com/setup_16.x | bash -
RUN apt-get install -y nodejs

# npmインストール
COPY ./src/frontend/package.json /workspace/src/frontend/
RUN npm install

WORKDIR /workspace/src/

COPY ./src/backend/requirements-dev.txt /workspace/src/backend/
RUN python3 -m pip install -r /workspace/src/backend/requirements-dev.txt

CMD ["sh"]