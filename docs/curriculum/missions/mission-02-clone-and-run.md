# Mission 2 — Clone `bytebangla-api` and run it locally

**Sprint:** 1 (Onboarding) · **Type:** Implementation · **Prerequisites:** Mission 1 · **Unlocks:** Mission 3

## Context

Your onboarding buddy has given you access to `bytebangla-api`, the backend service ByteBangla's
marketplace app talks to. Before changing anything, every engineer here is expected to get the service
running locally and read through the existing code — nobody edits a service they don't understand.

## Ticket

> **BYTE-102: Get `bytebangla-api` running locally**
> As a new backend engineer, I need to clone the repo, install its dependencies, and confirm the API
> responds locally before I pick up my first ticket.
> — filed by Engineering Manager

## Just-enough learning

- `git clone` and what a repository actually contains (code + history, not just files).
- What a `requirements.txt` / dependency manifest is for.
- What "running a dev server" means for a web API (`uvicorn` for FastAPI).
- Reading a repo's `README.md` first, before opening random files.

## Starter repository state

Repo: `content/build/starter-repo` (seeded at this exact state for Mission 2).

```
bytebangla-api/
  app/
    main.py        # FastAPI app with one route: GET / -> {"message": "ByteBangla API"}
    health.py       # GET /health -> currently returns {"status": "not implemented"} (Mission 3 fixes this)
  requirements.txt   # fastapi, uvicorn
  README.md          # minimal: how to install deps and run the dev server
```

## Work

1. Clone the repo.
2. Create a virtual environment and install dependencies from `requirements.txt`.
3. Start the dev server (`uvicorn app.main:app --reload`).
4. Confirm `GET /` returns `{"message": "ByteBangla API"}` in the browser or via `curl`.
5. Skim `app/main.py` and `app/health.py` — you'll need them next mission.

## Acceptance criteria

- [ ] Repository cloned locally.
- [ ] Dependencies installed with no errors.
- [ ] Dev server starts without crashing.
- [ ] `GET /` returns HTTP 200 with `{"message": "ByteBangla API"}`.

## Artifacts

- `bytebangla-api/` starter repo (read-only tour + run, no code change required yet).

## Hints

1. *Level 1:* `pip install -r requirements.txt` installs everything listed in that file at once.
2. *Level 2:* If `uvicorn` isn't found after installing, make sure your virtual environment is
   activated in the same terminal session you're running the command from.
3. *Level 3:* Exact run command: `uvicorn app.main:app --reload --port 8000`, then visit
   `http://localhost:8000/`.

## Submission

Command output / screenshot submission: paste the terminal output of starting the server and the
response body from `GET /`.

## Evaluation

Automated: platform can optionally spin up the repo and hit `GET /` server-side to confirm the learner's
environment produces the expected response; otherwise reviewed against the pasted output.

## Reflection prompt

"What's the difference between code that exists in a repository and code that's actually running? Why
did we ask you to do both today?"
