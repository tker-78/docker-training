# README

このレポジトリは、SPAアプリケーション構築のための
docker composeの雛形です。

```
docker compose up -d
```

システム構成: 
- frontend: Vuetify
- backend: FastAPI
- db:     PostgreSQL
- 認証: Keycloak


ポート番号:
- frontend: `localhost:5173`
- backend: `localhost:8000`
- db: `localhost:5432`
- 認証: `localhost:8080`
