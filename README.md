# README

このレポジトリは、SPAアプリケーション構築のための
docker composeの雛形です。

confidentialなclientとbackendのtoken交換については下記を参考にしました。(未実装)

[Shingen.py/doc_20250524](https://github.com/shingen-py/doc_20250524/tree/main)

## 実行手順

```
docker compose up -d
```

システム構成: 
- frontend: Vue3 + Vuetify
- backend: FastAPI
- db:     PostgreSQL
- 認証: Keycloak


ポート番号:
- frontend: `localhost:5173`
- backend: `localhost:8000`
- db: `localhost:5432`
- 認証: `localhost:8080`
