# ByteBangla Technologies — Simulated Company Spec

Source: Blueprint Section 5. Internal fictional company name; Code2Prod remains the education brand.

## What ByteBangla is

ByteBangla Technologies is a fictional marketplace / delivery platform (think: a local delivery or
services marketplace connecting customers, vendors, and riders). It exists purely so every mission has
a coherent, evolving product and codebase behind it — not as a role-play gimmick. Every artifact
(tickets, READMEs, PR templates, architecture diagrams, runbooks, logs, dashboards, postmortems, config
files, deployment manifests) should exist because a real team would plausibly produce it.

## Product surface (grows with the learner)

| Stage | What exists in the product |
|---|---|
| Free Foundations | Read-only tour: architecture diagram, a sample repo, a sample ticket, a sample incident. No code changes required. |
| BUILD | A single Python/FastAPI backend service (`bytebangla-api`) with users, listings/orders, and PostgreSQL persistence. |
| SHIP | The same service gains a Dockerfile, docker-compose for local dev, CI pipeline, and a staging deployment target. |
| OPERATE | The service is deployed via Kubernetes manifests/Helm, GitOps (ArgoCD-style), with Prometheus/Grafana observability. |
| PRODUCTION | The same running system is deliberately broken (config drift, bad deploy, resource exhaustion, data issue) for incident missions. |

The product never resets between courses — a BUILD graduate's repository is the SHIP starting point,
conceptually. For MVP, each course ships with its own pinned starter-repo state (see mission specs) so
courses can be developed and graded independently, but the fictional company, teams, and system stay
one continuous story.

## Teams (for narrative/ticket framing)

- **Product** — writes tickets, defines acceptance criteria, prioritizes the backlog.
- **Backend** — owns `bytebangla-api` (the learner's home team in BUILD).
- **QA** — writes/reviews test expectations, flags regressions.
- **DevOps** — owns CI/CD, container builds, releases (learner's home team in SHIP).
- **Platform** — owns Kubernetes, GitOps, observability tooling (learner's home team in OPERATE).
- **SRE** — owns on-call, incident response, postmortems (learner's home team in PRODUCTION).

## Environments

`local -> development -> staging -> production` — introduced progressively. BUILD only needs `local`.
SHIP introduces `staging`. OPERATE/PRODUCTION introduce full promotion and production-like behavior.

## Tone and realism rules

1. Never introduce a tool because it's popular — introduce it because ByteBangla hits a problem the
   tool solves (see `docs/curriculum/build-course-missions.md` sprint rationale).
2. Tickets should read like real tickets: a short title, context, acceptance criteria, and sometimes an
   irrelevant or slightly ambiguous detail — not a lab-manual instruction.
3. Incidents should give imperfect information and multiple plausible hypotheses, not a single obvious
   cause.
4. Keep company narrative light-touch. The learner should forget it's fictional within a few minutes of
   starting a mission.
