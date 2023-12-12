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

- .devcontainer : VSCodeのDev Containers向け各種定義ファイル
- .vscode : VSCode向け設定ファイル
- data : 初期設定では各種ユーザーデータ
- docs : 汎用的なドキュメント
- src : ソースコード
  - backend : バックエンドのソースコード
    - specs : バックエンド用テストコード
      - feature : 機能テスト用コード
      - unit : ユニットテスト用コード
    - yt_diffuser : バックエンドモジュール本体
  - frontend : フロントエンドのソースコード
    - public : 静的ファイル
    - specs : フロントエンド用テストコード
    - src : フロントエンドのソースコード

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

```
pytest --cov=yt_diffuser --cov-report html specs/
```