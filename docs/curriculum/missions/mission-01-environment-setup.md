# Mission 1 — Set up your engineering environment

**Sprint:** 1 (Onboarding) · **Type:** Implementation · **Prerequisites:** none · **Unlocks:** Mission 2

## Context

You just joined ByteBangla Technologies as a Junior Software Engineer on the Backend team. Before you
can touch any code, you need the same local setup every backend engineer here uses: Python 3.11+, Git,
and a terminal you're comfortable in. Your onboarding buddy (a senior engineer, represented in-product
by short text notes) has left you a checklist.

## Ticket

> **BYTE-101: New hire environment setup**
> As a new backend engineer, I need Python, Git, and a code editor configured so I can run and modify
> `bytebangla-api` locally.
> — filed by Engineering Manager

## Just-enough learning

- What a terminal/shell is and why engineers live in it.
- What Python + `pip`/`venv` (or `uv`) do and why services need isolated dependencies.
- What Git is at a one-paragraph level (full Git workflow is Mission 4).
- Why every engineer at a company runs the same language/tool versions (`.python-version`, lockfiles).

## Work

1. Install Python 3.11 or newer.
2. Install Git and set your name/email (`git config --global user.name/user.email`).
3. Install a code editor (VS Code recommended, not required).
4. Create a virtual environment and confirm `python --version` and `git --version` both run.

## Acceptance criteria

- [ ] `python3 --version` reports 3.11 or newer.
- [ ] `git --version` runs successfully.
- [ ] `git config --get user.name` and `git config --get user.email` are both set.
- [ ] A virtual environment can be created and activated without errors.

## Artifacts

- None yet (no repository access required for this mission).

## Hints

1. *Level 1:* Not sure how to check your Python version? Try `python3 --version` or `python --version`.
2. *Level 2:* On macOS, Python 3 often needs to be installed via `brew install python3` or from
   python.org — the system `python` may point to Python 2 or not exist.
3. *Level 3 (near-complete):* Full command sequence for macOS/Linux is provided in the platform's
   setup guide artifact; Windows learners are pointed to WSL2 setup instructions.

## Submission

Checklist submission: paste the output of `python3 --version`, `git --version`,
`git config --get user.name`. Automated check pattern-matches version numbers and non-empty config
values (no repo/CI needed for this mission).

## Evaluation

Automated only — pure environment/tooling check, no human review needed.

## Reflection prompt

"Why do you think a company would standardize on one Python version across all engineers, instead of
letting everyone use whatever they already have installed?"
