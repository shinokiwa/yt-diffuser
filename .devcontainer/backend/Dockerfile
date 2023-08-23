# NVIDIA CUDA 11.7 Ubuntu用をベースイメージにする
FROM nvidia/cuda:11.7.1-base-ubuntu22.04

# Install necessary system packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    language-pack-ja \
    build-essential \
    git curl \
    python3-pip python3-venv

# workspaceディレクトリを作成
WORKDIR /workspace/src/
RUN mkdir -p /workspace/src/backend /workspace/src/frontend

# Node.jsをインストール
RUN curl -sL https://deb.nodesource.com/setup_16.x | bash -
RUN apt-get install -y nodejs

# pipインストール
COPY ./src/backend/requirements.txt /workspace/src/backend/
RUN python3 -m pip install --no-cache-dir --upgrade pip setuptools wheel
RUN python3 -m pip install -r /workspace/src/backend/requirements.txt

COPY ./src/backend/requirements-dev.txt /workspace/src/backend/
RUN python3 -m pip install -r /workspace/src/backend/requirements-dev.txt

# npmインストール
COPY ./src/frontend/package.json /workspace/src/frontend/
RUN npm --prefix "/workspace/src/frontend" install /workspace/src/frontend
