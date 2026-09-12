# Mission 5 — Incident: "It works on my machine"

**Sprint:** 1 (Onboarding) · **Type:** Incident (mini) · **Prerequisites:** Mission 4 · **Unlocks:** Sprint 2, Mission 6

## Context

A teammate, Nusrat, pings you: she pulled the latest `main` (which now includes your Mission 3/4 fix)
and the server won't start on her machine, even though it works fine on yours. This is your first
taste of an "incident" mission — you're given symptoms and partial information, not a clean repro.

## Ticket / Page

> **Slack DM from Nusrat (Backend):**
> "hey, pulled main and now `uvicorn app.main:app --reload` just throws
> `ModuleNotFoundError: No module named 'fastapi'` right away. works fine for you?
> did something change in requirements?"

## Just-enough learning

- Why "it works on my machine" is one of the most common real bugs, not a joke.
- What a virtual environment isolates (and what happens when someone runs a command outside one).
- How to ask/gather the two or three facts that actually narrow down a bug like this.

## Starter repository state

Same repo as Mission 4. Nothing in the repository itself is broken — the "bug" is entirely in Nusrat's
local environment, which is described to the learner via the chat transcript above plus a follow-up
message if they ask for more detail (provided as a hint, see below).

## Work

1. Read Nusrat's message and form a hypothesis before asking for more information.
2. Ask (in the platform's chat-simulation UI, or write down) what you'd want to know next.
3. Diagnose: her virtual environment isn't activated, so `fastapi` isn't on her `PATH`.
4. Write back a short, concrete fix she can follow.

## Acceptance criteria

- [ ] Learner identifies "virtual environment not activated" (or equivalent: dependencies installed
      outside the venv) as the root cause, not a requirements.txt or code problem.
- [ ] Learner's reply to Nusrat includes a concrete command to activate the venv and reinstall/verify.
- [ ] Learner does not modify `requirements.txt` or any application code (there is nothing wrong with
      either).

## Artifacts

- Chat transcript (provided).
- Follow-up detail available as Hint Level 2: "oh wait, I don't think I see a `(venv)` in my prompt."

## Hints

1. *Level 1:* This error means Python can't find the `fastapi` package at all — what usually causes
   that, given the package installed fine for you?
2. *Level 2 (reveals extra info):* Nusrat mentions she doesn't see `(venv)` in her terminal prompt.
3. *Level 3 (near-complete):* The fix is: activate the virtual environment
   (`source venv/bin/activate`) before running `pip install -r requirements.txt` and `uvicorn`.

## Submission

Text diagnosis submission: root cause (one sentence) + the exact reply/fix given to Nusrat.

## Evaluation

Automated keyword/rubric check on the diagnosis (must name environment/activation, must not blame
requirements.txt or code) with mentor review available for ambiguous submissions.

## Reflection prompt

"You solved this without touching a single line of code. What does that tell you about what 'debugging'
actually means as an engineer?"
