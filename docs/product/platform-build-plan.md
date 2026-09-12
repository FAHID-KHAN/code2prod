# Platform Build Plan

How Code2Prod gets from today's repository to the first paid release.

Source of requirements: Code2Prod Founding Product Blueprint v0.1 — section references below
(§11 MVP scope, §13 identity, §14 payments, §16 admin, §19 data model, §20 security, §21 deployment,
§22 release process, §36 definition of done).

> **Sequencing note.** The blueprint's §37 "Founding principle" recommends authoring curriculum before
> building the platform. This plan deliberately builds the platform first. The one place that choice
> carries real engineering risk is Phase 4 (submissions/evaluation) — see the dependency called out
> there, and mitigate it by authoring missions 6-10 in parallel with Phases 2-3.

## Where things stand today

| §11 must-have for first paid launch | Status |
|---|---|
| Landing page and product explanation | **Done** — `apps/web`, static, dark design system |
| Email/password authentication | Not started |
| Free Foundations course | Not started (no content authored) |
| BUILD course with 20-30 missions | **Partial** — 25-mission backlog defined, 5 fully authored |
| Sprint/mission UI | Not started (design language exists and is reusable) |
| Markdown/code/diagram content | Not started |
| Progress tracking | Not started |
| Basic submission workflow | Not started |
| Payment + verified enrollment | Not started |
| Support tickets + live chat integration | Not started |
| Admin content management | Not started |
| Email + in-app notifications | Not started |
| Basic certificate / public evidence page | Not started |

What exists in `apps/api` today is a deliberately thin vertical slice: `Course -> Sprint -> Mission`
read models, three read-only endpoints, a hand-written seed, and 5 tests against SQLite. It proves the
shape; it is not yet the mission engine.

---

## Phase 0 — Make the codebase productionable

**Goal:** everything after this lands as a migration plus tested code.

- Replace `Base.metadata.create_all` (in `apps/api/app/main.py`) with **Alembic migrations**. §22
  requires migrations with rollback/forward-fix procedures. Doing this before any real user data
  exists is the entire point — retrofitting it later is a data-loss risk.
- CI on every PR: `ruff` + `mypy` + `pytest` for the API; `eslint` + `tsc` + `next build` for the web
  app. Protect `main`, require CI before merge (§22).
- `.env.example` committed, real secrets never in source control (§20).
- Structured JSON logging and an error-tracking hook (§17: "structured logs + error tracking first").
- Initial git commit and a conventional-commit convention.

**Exit criteria:** a fresh clone can migrate an empty database to current schema, CI blocks a failing
PR, and no secret is readable in the repository.

## Phase 1 — Identity and access

**Goal:** a `user_id` that every later domain can hang off.

- `users` and `profiles` tables (§19).
- Password hashing with Argon2 through a proven library. §17 is explicit: avoid building
  cryptography or session primitives yourself.
- Register → verify email → login → password reset, each rate-limited (§20).
- **Recommended:** httpOnly server-side sessions rather than JWT — revocation is trivial and the
  lifecycle is much harder to get wrong. See "Open decisions".
- Role enum from §13: `STUDENT`, `MENTOR`, `REVIEWER`, `SUPPORT_AGENT`, `CONTENT_CREATOR`, `ADMIN`,
  `SUPER_ADMIN`, enforced by a FastAPI dependency **server-side**, never merely hidden in the UI.
- CSRF protection for cookie-based state-changing requests (§20).

**Exit criteria:** a learner can register, verify, log in and reset a password; a `STUDENT` receives
403 from an admin-only endpoint even when calling the API directly.

## Phase 2 — Real content model and admin authoring

**Goal:** curriculum authors change missions without an engineering deploy (§16).

- Expand `Mission` from the current thin slice to the full §10 object: context, ticket, just-enough
  learning material, artifacts/assets, acceptance criteria, **progressive hints**, submission type,
  automated-check spec, evaluation mode, reflection/solution, prerequisites and unlock rules, and a
  `mission_type` enum (implementation, debugging, incident, code review, architecture, configuration,
  documentation, investigation).
- Add `course_versions` (§19) with draft/published states, so curriculum changes ship like releases
  (§18: "treat major curriculum changes like software releases").
- Admin CRUD for courses, versions, sprints and missions, with markdown/code/diagram attachments.
- Retire `app/seed/build_course.py` as a source of truth — it becomes bootstrap data only. Curriculum
  source stays mirrored in version control per §18.

**Exit criteria:** a `CONTENT_CREATOR` can author a complete mission end-to-end in the admin and
publish it, with no code change and no deploy.

## Phase 3 — Learner experience

**Goal:** the §12 "Mission" journey works: dashboard → sprint → mission → work → submit.

- `enrollments` (§19); free Foundations auto-enrolls on registration.
- Dashboard: enrolled courses, current sprint, next mission.
- Sprint and mission UI. The mission window built for the landing page is the proven design language —
  it gets wired to real data rather than redesigned.
- Prerequisites and unlock rules enforced server-side.
- **Progress must be event-oriented** (§19): record attempts, pass/fail/review states and timestamps.
  Never store a `percent_complete` column — preserve the evidence that produced the state.

**Exit criteria:** a learner completes an authored mission end-to-end and the dashboard reflects it
accurately after a refresh and a re-login.

## Phase 4 — Submissions and evaluation

**Goal:** the feedback loop that makes this a practice platform rather than a reader.

- `submissions` and `submission_results` (§19), with full attempt history and a retry loop.
- Submission types per §10: checklist, command output, text diagnosis, diff/commit, GitHub PR link,
  file upload.
- Automated checks driven by the check spec defined in Phase 2.
- Reviewer/mentor queue for human-evaluated submissions (§10: "automated tests plus human review
  where valuable").
- Safe upload handling and input validation (§20).

**Architectural constraint for v1: no untrusted learner code is executed.** Checks assert against
submitted evidence — pasted output, diffs, structured checklists, written diagnoses. Sandboxed
execution is the Labs phase (§31) and stays deferred; it is the single largest cost and security
risk in the product.

> **Dependency.** The check-spec design happens here, and only 5 missions are currently authored
> (three implementation, one debugging, one incident). Designing against that sample risks a check
> model that does not fit sprints 3-5 (persistence, quality, capstone). Author missions 6-10 during
> Phases 2-3 to de-risk this cheaply.

**Exit criteria:** a learner can fail a mission, read the feedback, retry, and pass — with every
attempt preserved and inspectable by a reviewer.

## Phase 5 — Payments and enrollment

**Goal:** money in, verified enrollment out, with no way to cheat it (§14).

- `orders`, `payments`, `enrollments`, `coupons`, `refunds` (§14 field lists).
- Order state machine: `ORDER(PENDING)` → gateway → validated callback → `PAYMENT(PAID)` →
  `ORDER(PAID)` → `ENROLLMENT(ACTIVE)`.
- SSLCOMMERZ behind a provider abstraction, sandbox first. Revalidate the provider's current
  documentation at implementation time (§40).
- BDT pricing, coupon support, order history, simple receipt.

**Non-negotiables (§14, §36):**

- Enrollment is created **only** after server-side validation of transaction, amount and currency.
- The browser reaching a success URL unlocks nothing.
- Callback processing is idempotent, keyed on `provider_transaction_id`.
- Every state transition is auditable.

**Exit criteria:** tests prove that duplicate, replayed, out-of-order and amount-mismatched callbacks
cannot produce a duplicate or incorrect enrollment.

## Phase 6 — Support, notifications, certificates

- `support_tickets` and `support_messages` with threaded replies (§15), separating educational
  support from billing support.
- Searchable markdown knowledge base.
- Third-party live-chat widget with **stated hours** — no 24/7 promise at launch (§15).
- Transactional email (verification, receipt, ticket reply) plus in-app notifications.
- Certificate issuance and the public evidence page (§11, §23).

**Exit criteria:** a learner can raise a ticket and get a threaded reply; support hours and ownership
are documented and visible.

## Phase 7 — Launch hardening

- Admin audit logs (§19) and mandatory admin MFA (§13).
- Database backups **with a tested restore** (§20) — an untested backup is not a backup.
- Uptime monitoring, error tracking, structured logs (§21).
- Terms, privacy policy, pricing and refund rules published (§20).
- Deployment per §21: managed Next.js hosting/CDN, managed container platform for the API, managed
  PostgreSQL. Explicitly **not** self-managed Kubernetes — Kubernetes being in the curriculum is not
  a reason to run the platform on it.
- Staging environment, smoke tests, traceable versioned deploys, rollback runbook (§22).
- Incident runbooks for payment outage, login outage and database failure (§22).
- Walk the §36 "First Paid Release — Definition of Done" checklist before launch.

---

## Open decisions

These need a call before the phase that depends on them:

| Decision | Phase | Recommendation |
|---|---|---|
| Sessions vs JWT | 1 | httpOnly server-side sessions — simpler revocation |
| Auth in-house vs library/service | 1 | Proven library; §17 warns against rolling your own |
| Admin location | 2 | `/admin` inside the web app, role-gated |
| Content source of truth | 2 | Database, exported to version control for history |
| Redis | 3-4 | Only when a real queue/cache need appears (§17) |

## Known debt to retire along the way

- `Base.metadata.create_all` on startup → Alembic (Phase 0).
- `app/seed/build_course.py` duplicates `docs/curriculum/build-course-missions.md` by hand → admin
  authoring (Phase 2).
- `apps/web/src/components/CoursePath.tsx` hardcodes the five stages that the API already serves →
  single source of truth (Phase 3).
- No `packages/` shared layer yet, deliberately. Add it when duplication between web and api is real,
  not before.
