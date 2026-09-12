# BUILD Course — Mission Backlog (25 missions)

Role: Junior Software Engineer at ByteBangla Technologies (Backend team).
Objective: build and maintain `bytebangla-api` while learning Git, Linux, Python, APIs, and PostgreSQL
in context. Per blueprint Section 7 / 37: this backlog is written **before** any platform code, so the
mission engine's real requirements come from real content, not guesses.

Pedagogical pattern per mission: Context -> Requirement -> Just-enough explanation -> Work ->
Acceptance criteria -> Automated checks -> Feedback -> Reflection.

Rule: a tool/concept appears only when ByteBangla has a problem it solves — see "Why now" column.

## Sprint 1 — Onboarding (Linux, Git, repository workflow)

| # | Mission | Type | Why now |
|---|---|---|---|
| 1 | Set up your engineering environment | Implementation | You can't do any of the work below without a working local setup — first-day-on-the-job framing. |
| 2 | Clone `bytebangla-api` and run it locally | Implementation | Reading and running code before writing any is how real onboarding works. |
| 3 | Fix your first bug: the `/health` check lies | Debugging | Cheapest possible real bug — teaches reading a traceback and the repo layout. |
| 4 | Ship your first change via a pull request | Implementation | Branches/PRs are introduced the moment there's a real change to submit, not as an abstract Git lesson. |
| 5 | Incident: "It works on my machine" | Incident (mini) | A teammate's environment issue — first taste of environment drift before persistence/config exist to make it interesting. |

## Sprint 2 — APIs (Python, FastAPI, HTTP, JSON, REST)

| # | Mission | Type | Why now |
|---|---|---|---|
| 6 | Add a real `/health` endpoint | Implementation | Product needs uptime monitoring to exist before it's worth building anything else. |
| 7 | Build `GET /users/{id}` | Implementation | The company's first real read endpoint; introduces path params, JSON responses, status codes. |
| 8 | Add input validation and error responses | Implementation | QA files a bug: bad input crashes the server with a 500. Introduces Pydantic validation and consistent error shape. |
| 9 | Build `POST /users` | Implementation | Company needs to actually create users, not just read seed data. |
| 10 | Add pagination to `GET /users` | Implementation | Product complains the endpoint returns everyone at once as the seed data grows — realistic scale trigger. |

## Sprint 3 — Persistence (SQL, data modelling, ORM, connection strings)

| # | Mission | Type | Why now |
|---|---|---|---|
| 11 | Design the `users` table | Architecture | In-memory data disappears on every restart — product escalates a data-loss complaint. |
| 12 | Connect the API to PostgreSQL | Configuration | Introduces connection strings and env-based config because the app now depends on external state. |
| 13 | Migrate users from memory to PostgreSQL | Implementation | Wires the ORM (SQLAlchemy) into the endpoints built in Sprint 2. |
| 14 | Add `orders` with a foreign key to `users` | Implementation | Company launches its first real feature (orders) — introduces relational modelling. |
| 15 | Debug: the order list is missing rows | Debugging | A seeded migration/query bug (e.g. wrong join) — first real data debugging task. |

## Sprint 4 — Quality (pytest, logging, env vars, README, defensive coding)

| # | Mission | Type | Why now |
|---|---|---|---|
| 16 | Write tests for the users endpoints | Implementation | A regression shipped in Sprint 3 (seeded) — company mandates tests before further changes. |
| 17 | Add structured logging | Implementation | Support can't tell what happened during the Sprint 3 bug — logs introduced to solve a real diagnosis problem. |
| 18 | Externalize configuration | Configuration | Hardcoded DB credentials were just found in the repo — introduces `.env` and 12-factor config. |
| 19 | Write the service README / runbook | Documentation | A new teammate (fictional) can't get the service running from the repo alone. |
| 20 | Incident: staging won't start | Incident (mini) | A bad env var (seeded) breaks startup — first mission solved primarily by reading logs, not code. |

## Sprint 5 — Final build (full ticket-to-review workflow)

| # | Mission | Type | Why now |
|---|---|---|---|
| 21 | Ticket: implement "cancel order" | Implementation | First feature driven by a full ticket with acceptance criteria and edge cases, no hand-holding. |
| 22 | Code review: review a teammate's PR | Code review | Company culture requires review before merge — learner sits on the other side of a PR for once. |
| 23 | Harden edge cases flagged by QA | Debugging | QA files three bug reports against mission 21's feature — realistic post-review cleanup. |
| 24 | Release polish: docs, tests, cleanup | Documentation | Nothing ships without docs/tests at ByteBangla — reinforces Sprint 4 habits under a deadline. |
| 25 | Capstone: ship a feature end-to-end | Implementation (capstone) | Ticket -> branch -> code -> tests -> docs -> PR -> review -> merge, unaided, as the BUILD exit bar. |

## Mission count vs. blueprint target

25 missions, 2 incidents (missions 5 and 20), 1 capstone (mission 25) — matches Section 7's target of
"roughly 20-30 missions, two small incidents and one final project."

## Fully authored missions (first five)

See `docs/curriculum/missions/mission-01..05.md` for complete specs (context, ticket, acceptance
criteria, starter repo state, hints, submission type). Missions 6-25 are scoped above at backlog level
and get fully authored the same way before the mission engine's schema is frozen.
