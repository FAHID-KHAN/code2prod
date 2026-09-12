# MVP Architecture — Simplest BUILD Stage

Source: Blueprint Sections 17-19, scoped down to what BUILD (+landing page) actually needs right now.
This is deliberately smaller than the full north-star architecture in Section 39 — we add pieces only
when a real course stage needs them, same rule as the curriculum itself.

## What exists today

```
Internet
  -> apps/web (Next.js)         marketing site + free mission preview
  -> apps/api (FastAPI)          read-only mission engine (courses/sprints/missions)
       -> PostgreSQL              via infrastructure/docker/docker-compose.yml
```

The API is a genuine modular monolith, but deliberately thin: it serves the BUILD course backlog
(read-only) because that's the only content fully specified so far. No auth, no submissions/grading, no
payments — those domains get added once the missions that need them (submission workflow, enrollment)
are themselves fully authored, per the "curriculum discovery drives platform requirements" principle.

## What BUILD (rest of Phase 1) still requires

```
Internet
  -> apps/web (Next.js)        learner dashboard, mission UI, auth
  -> apps/api (FastAPI)         + auth, submissions, enrollments domains
  -> PostgreSQL                  users, enrollments, submissions
  -> Object storage              mission assets (later)
```

One deployable API service internally organized by domain (`app/domains/<name>/`), not separate
microservices — see Section 17-18: "early scale does not justify operationally independent services."

## Repository layout (current)

```
code2prod/
  apps/
    web/                       Next.js app (landing page today, learner app later)
    api/                       FastAPI modular monolith
      app/
        core/                  settings, db session
        domains/
          health/
          courses/             Course -> Sprint -> Mission read model
        seed/                  seeds the BUILD backlog (transitional, no admin panel yet)
      tests/
  content/
    build/
      starter-repo/            the actual bytebangla-api starter code missions 1-5 reference
  docs/
    product/                   persona, product promise
    curriculum/                 company spec, mission backlog, fully authored missions
    architecture/               this file
  infrastructure/
    docker/                    docker-compose.yml (local Postgres)
  README.md
```

`packages/` (shared UI/schemas between web and api) is deliberately not created yet — there is nothing
to share between a static marketing page and a read-only API today. Add it when a real duplication
appears, not before.

## Deliberately deferred (per Section 11)

Browser-based cloud labs, microservices, native apps, 24/7 support, AI mentor, recruiter marketplace,
Kubernetes deployment of the platform itself. None of these are needed to prove the core thesis: do
learners finish realistic work and want to pay for the next stage.
