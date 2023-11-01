# yt-diffuser
YuTori Diffuser

## テスト実行

### フロントエンド

Vitestを使います。

```
> cd src/frontend
> npm run test
```

### バックエンド

Pytestを使います。

```
> cd src/backend
> pytest specs/path/to/test
```

カバレッジ取得は以下。

```
> pytest --cov=yt_diffuser --cov-report html specs/
```