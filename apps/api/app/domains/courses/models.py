from sqlalchemy import JSON, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(50), unique=True)
    name: Mapped[str] = mapped_column(String(100))
    role: Mapped[str] = mapped_column(String(100))
    is_free: Mapped[bool] = mapped_column(default=False)
    price_bdt_min: Mapped[int | None] = mapped_column(default=None)
    price_bdt_max: Mapped[int | None] = mapped_column(default=None)

    sprints: Mapped[list["Sprint"]] = relationship(
        back_populates="course", order_by="Sprint.order", cascade="all, delete-orphan"
    )


class Sprint(Base):
    __tablename__ = "sprints"

    id: Mapped[int] = mapped_column(primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"))
    name: Mapped[str] = mapped_column(String(100))
    order: Mapped[int]

    course: Mapped[Course] = relationship(back_populates="sprints")
    missions: Mapped[list["Mission"]] = relationship(
        back_populates="sprint", order_by="Mission.number", cascade="all, delete-orphan"
    )


class Mission(Base):
    __tablename__ = "missions"

    id: Mapped[int] = mapped_column(primary_key=True)
    sprint_id: Mapped[int] = mapped_column(ForeignKey("sprints.id"))
    number: Mapped[int]
    title: Mapped[str] = mapped_column(String(200))
    mission_type: Mapped[str] = mapped_column(String(50))

    # Fully authored content is optional: early missions (1-5) have it,
    # later backlog missions (6-25) don't yet — see docs/curriculum.
    context: Mapped[str | None] = mapped_column(default=None)
    ticket: Mapped[str | None] = mapped_column(default=None)
    acceptance_criteria: Mapped[list[str] | None] = mapped_column(JSON, default=None)
    submission_type: Mapped[str | None] = mapped_column(String(100), default=None)

    sprint: Mapped[Sprint] = relationship(back_populates="missions")
