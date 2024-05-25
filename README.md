# ゆとりでふーざー

YuTori Diffuser<br />
結城真がとりあえず作った拡散モデルアプリ。

趣味で作ってるだけのただの習作。

## 使い方

まだ書いてない！

## 基本構成

バックエンドはPythonとFlaskを使ったWeb API、フロントエンドはVue.jsを使ったSPAになっている。<br>
**現段階ではインターネットへの公開は想定しておらず、セキュリティは確保されていないので注意。**

## ディレクトリ構成

[こちら](./docs/directories.md)を参照。


## 開発環境について

Visual Studio CodeのDev Containersを推奨。<br>
.devcontainerに一通りの設定が入っているため、自動構築できる。<br>
環境の詳細については./devcontaienr/docker-compose.ymlを参照。

## テスト実行について

### フロントエンド

Vitestを使用。

```
cd src/frontend
npm run test
```

### バックエンド

Pytestを使用。

```
cd src/backend
pytest specs/path/to/test
```

カバレッジ取得は以下。

```sh
# ターミナルにレポートを出力する場合
pytest --cov=yt_diffuser --cov-report term-missing specs/


# HTMLファイルに出力する場合
pytest --cov=yt_diffuser --cov-report html specs/
```