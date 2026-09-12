# Code2Prod

> Your first engineering job should not be your first experience doing real engineering work.

This repo follows the founding product blueprint's own sequencing (`docs/product`,
`docs/curriculum` before platform code — see "Founding principle" in the blueprint): curriculum
discovery drives platform requirements, not the other way around.

## What's here

| Path | What it is |
|---|---|
| `docs/product/` | Learner persona and product promise |
| `docs/curriculum/` | ByteBangla company spec, the full 25-mission BUILD backlog, and fully authored specs for missions 1-5 |
| `docs/architecture/` | Current + near-term system architecture |
| `content/build/starter-repo/` | The actual `bytebangla-api` starter code that missions 1-5 reference |
| `apps/web/` | Next.js landing page — pitches Code2Prod and embeds a real, interactive sample mission |
| `apps/api/` | FastAPI modular monolith — currently a read-only mission engine serving the BUILD backlog |
| `infrastructure/docker/` | Local Postgres via docker-compose |

## Run it

**Landing page**

```bash
cd apps/web
pnpm install
pnpm dev
```

**API**

```bash
docker compose -f infrastructure/docker/docker-compose.yml up -d
cd apps/api
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env
alembic upgrade head
python -m app.seed
uvicorn app.main:app --reload
```

See [apps/api/README.md](apps/api/README.md) for migrations, checks and layout.

## Contributing

- CI (`.github/workflows/ci.yml`) runs lint, type checks, tests and migrations for both apps on every
  pull request. Keep `main` protected and require CI before merge.
- Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/):
  `feat:`, `fix:`, `chore:`, `docs:`, `refactor:`, `test:`.

## What's next

Per `docs/curriculum/build-course-missions.md`, missions 6-25 are scoped at backlog level but not yet
fully authored. The next real step is authoring them the way missions 1-5 were authored (context,
ticket, acceptance criteria, starter repo state) — that's what will tell us what the submissions,
grading, and enrollment domains in `apps/api` actually need to look like.
