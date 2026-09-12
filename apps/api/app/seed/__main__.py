"""Seed bootstrap content: `python -m app.seed`.

Run explicitly after `alembic upgrade head`. Seeding is idempotent, and is not run
on application startup — a boot should never write content.
"""

import logging

from app.core.db import SessionLocal
from app.core.logging import configure_logging
from app.seed.build_course import seed_build_course


def main() -> None:
    configure_logging()
    logger = logging.getLogger("app.seed")

    with SessionLocal() as db:
        course = seed_build_course(db)
        mission_count = sum(len(sprint.missions) for sprint in course.sprints)

    logger.info(
        "seed complete",
        extra={
            "course": course.slug,
            "sprints": len(course.sprints),
            "missions": mission_count,
        },
    )


if __name__ == "__main__":
    main()
