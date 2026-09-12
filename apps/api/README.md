# Code2Prod API

FastAPI modular monolith. See `docs/architecture/mvp-architecture.md` at the repo root for how this
fits into the overall system, and `docs/product/platform-build-plan.md` for what gets built next.

## Run locally

```bash
docker compose -f ../../infrastructure/docker/docker-compose.yml up -d

python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env

alembic upgrade head      # apply schema
python -m app.seed        # load bootstrap content (idempotent)

uvicorn app.main:app --reload --port 8000
```

The app never creates or alters tables at startup — schema changes only ever happen through
`alembic upgrade`, so a rollout cannot silently reshape the database. Seeding is likewise explicit.

Try it:

```bash
curl http://localhost:8000/health
curl http://localhost:8000/courses
curl http://localhost:8000/courses/build
curl http://localhost:8000/courses/build/missions/3
```

## Checks

```bash
ruff check .        # lint
mypy                # types (strict)
pytest -q           # tests
alembic check       # fails if models drift from migrations
```

Tests build their schema by running the real migrations against a temporary SQLite database, so a
broken or missing migration fails the suite rather than production.

## Migrations

```bash
alembic revision --autogenerate -m "describe the change"
alembic upgrade head
alembic downgrade -1
```

Autogenerate only sees models that are imported in `migrations/env.py` — add an import there when you
introduce a new domain, or its tables will be silently missing from migrations.

## Layout

```
app/
  core/          settings, database session, logging, middleware, security, rate limiting
  domains/
    health/      liveness endpoint
    auth/        users, profiles, JWT + rotating refresh tokens, RBAC
    courses/     Course -> Sprint -> Mission read model
  seed/          bootstrap content (python -m app.seed)
migrations/      alembic
tests/
```

## Authentication

Access tokens are stateless 15-minute JWTs sent as `Authorization: Bearer …`. Refresh tokens are
opaque, stored hashed, and rotate on every use; presenting an already-rotated token is treated as a
leak and revokes that token's whole family. The refresh token rides in an httpOnly `SameSite=Strict`
cookie for browsers, and an `x-refresh-token` header is accepted for native clients.

Because access tokens are verified without a database lookup, revoking a session takes effect on the
refresh token immediately but on the access token only when it expires — hence the short TTL. The
user's role, however, *is* re-read per request, so demotions and deactivations apply instantly.

Email is written to the log rather than sent until a provider is wired up, so verification and reset
tokens are readable in local output.

## What's here vs. what's next

This is the vertical slice that serves the BUILD mission backlog — see
`docs/curriculum/build-course-missions.md`. Auth, submissions/grading, payments and enrollments are
not built yet; `docs/product/platform-build-plan.md` sequences them.
