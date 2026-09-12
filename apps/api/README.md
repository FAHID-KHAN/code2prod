# Code2Prod API

FastAPI modular monolith. See `docs/architecture/mvp-architecture.md` at the repo root for how this
fits into the overall system.

## Run locally against Postgres

```bash
docker compose -f ../../infrastructure/docker/docker-compose.yml up -d
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
uvicorn app.main:app --reload --port 8000
```

On startup the app creates tables and seeds the BUILD course from
`app/seed/build_course.py`. Try:

```bash
curl http://localhost:8000/health
curl http://localhost:8000/courses
curl http://localhost:8000/courses/build
curl http://localhost:8000/courses/build/missions/3
```

## Tests

Tests run against a temporary SQLite file, no Docker required:

```bash
pytest
```

## What's here vs. what's next

This is the vertical slice needed to serve the BUILD mission backlog (25 missions, fully authored
detail for missions 1-5) — see `docs/curriculum/build-course-missions.md`. Auth, submissions/grading,
payments, and enrollments are intentionally not built yet; they get added once the corresponding
missions (6-25) are fully authored, per the blueprint's "curriculum discovery drives platform
requirements" principle.
