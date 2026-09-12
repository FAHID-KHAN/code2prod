# Mission 4 — Ship your first change via a pull request

**Sprint:** 1 (Onboarding) · **Type:** Implementation · **Prerequisites:** Mission 3 · **Unlocks:** Mission 5

## Context

Fixing `/health` locally isn't enough — at ByteBangla, no change reaches other engineers or production
without a pull request and at least one review. Today you'll take the fix from Mission 3 through the
same branch → commit → PR flow every engineer here uses, even for one-line changes.

## Ticket

> **BYTE-104: Submit the `/health` fix as a pull request**
> As a backend engineer, I need to open a PR for BYTE-103 so it can be reviewed and merged following
> team process, not just applied locally.
> — filed by Engineering Manager

## Just-enough learning

- Why teams use branches instead of committing straight to `main`.
- What a commit is (a snapshot + message), and what makes a good commit message.
- What a pull request is: a request to merge your branch, with a diff reviewers can read.
- Reading a PR template / description and what reviewers look for (does the diff match the ticket?).

## Starter repository state

Same repo as Mission 3, now with your Mission 3 fix already applied locally (uncommitted).

## Work

1. Create a branch named `fix/health-check-status`.
2. Commit your Mission 3 change with a clear message referencing `BYTE-103`.
3. Push the branch and open a pull request against `main`.
4. Fill in the PR description: what changed, why, and how you verified it (link back to BYTE-103).

## Acceptance criteria

- [ ] Change exists on a branch, not committed directly to `main`.
- [ ] Commit message references `BYTE-103` and describes the change in the imperative mood
      (e.g. "Fix /health to return ok status").
- [ ] PR description explains what changed and how it was verified.
- [ ] PR diff contains only the `app/health.py` change — no unrelated files.

## Artifacts

- Git branch + PR (simulated via the platform's Git integration, or a real GitHub repo in MVP+).

## Hints

1. *Level 1:* `git checkout -b fix/health-check-status` creates and switches to a new branch in one
   step.
2. *Level 2:* A good commit message says what changed and why, not just "fix bug."
3. *Level 3:* Example commit message: `Fix /health to return ok status (BYTE-103)` with a body line
   explaining the monitor was silently broken.

## Submission

GitHub PR/commit submission: link to the PR (or, pre-GitHub-integration, the branch name + commit hash
+ pasted PR description).

## Evaluation

Automated: checks branch name pattern, commit message references the ticket ID, diff is scoped to the
expected file. Human/mentor spot-check optional at this stage.

## Reflection prompt

"What would go wrong at a company of 50 engineers if everyone just pushed straight to `main` instead of
using branches and PRs?"
