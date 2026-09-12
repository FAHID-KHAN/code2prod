"""Seed data for the BUILD course.

Mirrors docs/curriculum/build-course-missions.md and the fully authored specs in
docs/curriculum/missions/. There is no content-admin pipeline yet (see blueprint
Section 16), so this is duplicated by hand for now — it should be replaced by a
real content source once the admin panel exists.
"""

from sqlalchemy.orm import Session

from app.domains.courses.models import Course, Mission, Sprint

# (number, title, mission_type) for every mission in the backlog.
_BACKLOG: list[tuple[int, str, str]] = [
    (1, "Set up your engineering environment", "implementation"),
    (2, "Clone bytebangla-api and run it locally", "implementation"),
    (3, "Fix your first bug: the /health check lies", "debugging"),
    (4, "Ship your first change via a pull request", "implementation"),
    (5, 'Incident: "It works on my machine"', "incident"),
    (6, "Add a real /health endpoint", "implementation"),
    (7, "Build GET /users/{id}", "implementation"),
    (8, "Add input validation and error responses", "implementation"),
    (9, "Build POST /users", "implementation"),
    (10, "Add pagination to GET /users", "implementation"),
    (11, "Design the users table", "architecture"),
    (12, "Connect the API to PostgreSQL", "configuration"),
    (13, "Migrate users from memory to PostgreSQL", "implementation"),
    (14, "Add orders with a foreign key to users", "implementation"),
    (15, "Debug: the order list is missing rows", "debugging"),
    (16, "Write tests for the users endpoints", "implementation"),
    (17, "Add structured logging", "implementation"),
    (18, "Externalize configuration", "configuration"),
    (19, "Write the service README / runbook", "documentation"),
    (20, "Incident: staging won't start", "incident"),
    (21, 'Ticket: implement "cancel order"', "implementation"),
    (22, "Code review: review a teammate's PR", "code_review"),
    (23, "Harden edge cases flagged by QA", "debugging"),
    (24, "Release polish: docs, tests, cleanup", "documentation"),
    (25, "Capstone: ship a feature end-to-end", "implementation"),
]

_SPRINTS: list[tuple[str, range]] = [
    ("Onboarding", range(1, 6)),
    ("APIs", range(6, 11)),
    ("Persistence", range(11, 16)),
    ("Quality", range(16, 21)),
    ("Final build", range(21, 26)),
]

# Full detail for the fully authored missions (1-5). See
# docs/curriculum/missions/mission-0{n}-*.md for the complete spec.
_MISSION_DETAIL: dict[int, dict] = {
    1: {
        "context": (
            "You just joined ByteBangla Technologies as a Junior Software Engineer "
            "on the Backend team. Before you can touch any code, you need the same "
            "local setup every backend engineer here uses."
        ),
        "ticket": (
            "BYTE-101: New hire environment setup. As a new backend engineer, I need "
            "Python, Git, and a code editor configured so I can run and modify "
            "bytebangla-api locally."
        ),
        "acceptance_criteria": [
            "python3 --version reports 3.11 or newer",
            "git --version runs successfully",
            "git config user.name and user.email are both set",
            "A virtual environment can be created and activated without errors",
        ],
        "submission_type": "checklist",
    },
    2: {
        "context": (
            "Your onboarding buddy has given you access to bytebangla-api. Before "
            "changing anything, every engineer here is expected to get the service "
            "running locally and read through the existing code."
        ),
        "ticket": (
            "BYTE-102: Get bytebangla-api running locally. As a new backend engineer, "
            "I need to clone the repo, install its dependencies, and confirm the API "
            "responds locally before I pick up my first ticket."
        ),
        "acceptance_criteria": [
            "Repository cloned locally",
            "Dependencies installed with no errors",
            "Dev server starts without crashing",
            'GET / returns HTTP 200 with {"message": "ByteBangla API"}',
        ],
        "submission_type": "command_output",
    },
    3: {
        "context": (
            "ByteBangla's uptime monitor pings /health every 30 seconds and pages "
            "on-call if it doesn't return ok. QA just noticed the endpoint always "
            'reports "not implemented".'
        ),
        "ticket": (
            'BYTE-103: /health always returns "not implemented". As the on-call '
            'engineer, I need /health to return {"status": "ok"} when the service is '
            "actually healthy, so the uptime monitor is meaningful."
        ),
        "acceptance_criteria": [
            "GET /health returns HTTP 200",
            'Response body is exactly {"status": "ok"}',
            "No other endpoint's behavior changed",
        ],
        "submission_type": "diff",
    },
    4: {
        "context": (
            "Fixing /health locally isn't enough — at ByteBangla, no change reaches "
            "other engineers or production without a pull request and at least one "
            "review."
        ),
        "ticket": (
            "BYTE-104: Submit the /health fix as a pull request. As a backend "
            "engineer, I need to open a PR for BYTE-103 so it can be reviewed and "
            "merged following team process."
        ),
        "acceptance_criteria": [
            "Change exists on a branch, not committed directly to main",
            "Commit message references BYTE-103 in the imperative mood",
            "PR description explains what changed and how it was verified",
            "PR diff contains only the app/health.py change",
        ],
        "submission_type": "pull_request",
    },
    5: {
        "context": (
            "A teammate, Nusrat, pulled the latest main and the server won't start "
            "on her machine, even though it works fine on yours."
        ),
        "ticket": (
            "Slack DM from Nusrat: pulled main and now uvicorn throws "
            "ModuleNotFoundError: No module named 'fastapi' right away. Works fine "
            "for you? Did something change in requirements?"
        ),
        "acceptance_criteria": [
            "Learner identifies the venv not being activated as the root cause",
            "Reply includes a concrete command to activate the venv and verify",
            "Learner does not modify requirements.txt or application code",
        ],
        "submission_type": "text_diagnosis",
    },
}


def seed_build_course(db: Session) -> Course:
    """Insert the BUILD course if it doesn't already exist, and return it."""
    existing = db.query(Course).filter_by(slug="build").one_or_none()
    if existing is not None:
        return existing

    course = Course(
        slug="build",
        name="BUILD",
        role="Junior Software Engineer",
        is_free=False,
        price_bdt_min=599,
        price_bdt_max=799,
    )

    missions_by_number = {number: (title, mission_type) for number, title, mission_type in _BACKLOG}

    for order, (sprint_name, mission_numbers) in enumerate(_SPRINTS):
        sprint = Sprint(name=sprint_name, order=order)
        for number in mission_numbers:
            title, mission_type = missions_by_number[number]
            detail = _MISSION_DETAIL.get(number, {})
            sprint.missions.append(
                Mission(
                    number=number,
                    title=title,
                    mission_type=mission_type,
                    context=detail.get("context"),
                    ticket=detail.get("ticket"),
                    acceptance_criteria=detail.get("acceptance_criteria"),
                    submission_type=detail.get("submission_type"),
                )
            )
        course.sprints.append(sprint)

    db.add(course)
    db.commit()
    db.refresh(course)
    return course
