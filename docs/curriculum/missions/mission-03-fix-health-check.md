# Mission 3 — Fix your first bug: the `/health` check lies

**Sprint:** 1 (Onboarding) · **Type:** Debugging · **Prerequisites:** Mission 2 · **Unlocks:** Mission 4

## Context

ByteBangla's uptime monitor pings `/health` every 30 seconds and pages on-call if it doesn't return
`{"status": "ok"}`. QA just noticed the endpoint always reports `{"status": "not implemented"}` —
harmless today, but it means the monitor can never actually detect a real outage. Your onboarding buddy
assigned it to you as a low-risk first bug.

## Ticket

> **BYTE-103: `/health` always returns "not implemented"**
> As the on-call engineer, I need `/health` to return `{"status": "ok"}` when the service is actually
> healthy, so the uptime monitor is meaningful.
> — filed by QA

## Just-enough learning

- Reading a small Python function and tracing what it returns.
- What a health check endpoint is for and why it must be cheap/fast (no heavy logic yet).
- Editing code, saving, and seeing `--reload` pick up the change automatically.

## Starter repository state

Same repo as Mission 2, `app/health.py` currently contains:

```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "not implemented"}
```

## Work

1. Open `app/health.py`.
2. Change the handler so it returns `{"status": "ok"}`.
3. Restart (or let `--reload` restart) the dev server and confirm the fix with `curl` or the browser.

## Acceptance criteria

- [ ] `GET /health` returns HTTP 200.
- [ ] Response body is exactly `{"status": "ok"}`.
- [ ] No other endpoint's behavior changed.

## Artifacts

- `bytebangla-api/app/health.py`

## Hints

1. *Level 1:* The function's return value is a Python dict — what does it currently return, and what
   should it return instead?
2. *Level 2:* You only need to change the string value, not the structure of the dict.
3. *Level 3:* The full fixed line is `return {"status": "ok"}`.

## Submission

GitHub-style diff/commit submission: paste the one-line diff (or full file) showing the fix.

## Evaluation

Automated: a test hits `GET /health` and asserts the response equals `{"status": "ok"}`.

## Reflection prompt

"This was a one-line fix. Why do you think a company would still want it to go through a ticket, a
diff, and a check instead of just being edited directly on the running server?"
