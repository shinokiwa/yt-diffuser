# 細かいTIPS

## GPUが搭載されていないマシンで開発するとき

.devcontainer/docker-compose.yml を編集して、backendとdevcontainerの「devices」ディレクティブを削除する。<br>
編集を間違ってGitにコミットしないようにするには、以下のコマンド。

```sh
git update-index --assume-unchanged .devcontainer/docker-compose.yml
```

戻す場合は以下。

```sh
git update-index --no-assume-unchanged .devcontainer/docker-compose.yml
```
