# Repository Guidelines

## Project Structure & Module Organization
This repository packages a dockerized SPA stack. `frontend/ui` houses the Vite-powered Vue 3 + Vuetify app; shared plugins live in `src/plugins`, routing logic in `src/router`, and auth helpers like `keycloak.ts` in `src`. `backend/app` contains the FastAPI service, currently centered on Keycloak callbacks—add future modules under `backend/app/<feature>` with snake_case names. `docker-compose.yml` orchestrates the `front`, `api`, PostgreSQL, and Keycloak services; tune container-level environment variables here and keep supporting docs under `docs/`.

## Build, Test, and Development Commands
Run `docker compose up --build` to start the full stack, and `docker compose down` (or `docker compose stop`) when finished. Frontend work happens in `frontend/ui`: install dependencies once with `npm install`, then use `npm run dev` for hot reload, `npm run build` for production assets, and `npm run lint` to apply ESLint + Vuetify rules. For backend iteration, rely on the compose-managed Uvicorn process or open a shell with `docker compose exec api bash` to run ad-hoc scripts.

## Coding Style & Naming Conventions
Frontend TypeScript uses two-space indentation inside Vue SFCs, PascalCase component filenames, and kebab-case route paths. Keep Vue script blocks typed and prefer composables for shared logic. Backend Python follows PEP 8 with four-space indentation, explicit type hints, and descriptive snake_case modules; add docstrings for new endpoints. Store secrets in `.env` files loaded via `python-dotenv`, and never hardcode credentials.

## Testing Guidelines
Automated suites are not yet committed. When adding coverage, place backend tests under `backend/tests/` and target pytest with files named `test_<feature>.py`. Frontend tests should use Vitest (compatible with Vite) under `frontend/ui/src/__tests__`, wrapping components with Vuetify setup utilities. Always pair automated checks with a manual sign-in through `http://localhost:5173` to validate Keycloak token flows.

## Commit & Pull Request Guidelines
Mirror the existing history: concise, present-tense summaries (English or Japanese) such as `add keycloak callback handler`. Reference related issues, list impacted services (`front`, `api`, `db`, `keycloak`), and call out required env or data migrations. PRs should note UI-visible changes with screenshots and describe how to reproduce auth flows locally.

## Security & Configuration Tips
Never commit `.env` files or Keycloak secrets; instead, document setup steps in `docs/tips.md` and share credentials through secure channels. Refresh Keycloak client secrets when rotating environments and update the corresponding env vars consumed in `backend/app/main.py`. Before bumping base images, confirm persistent Postgres volume compatibility to avoid data loss.
