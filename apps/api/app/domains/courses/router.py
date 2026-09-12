from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.domains.courses.models import Course, Mission
from app.domains.courses.schemas import CourseDetail, CourseSummary, MissionDetail

router = APIRouter(prefix="/courses", tags=["courses"])


@router.get("", response_model=list[CourseSummary])
def list_courses(db: Session = Depends(get_db)) -> list[Course]:
    return list(db.scalars(select(Course).order_by(Course.id)))


@router.get("/{slug}", response_model=CourseDetail)
def get_course(slug: str, db: Session = Depends(get_db)) -> Course:
    course = db.scalar(select(Course).where(Course.slug == slug))
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@router.get("/{slug}/missions/{number}", response_model=MissionDetail)
def get_mission(slug: str, number: int, db: Session = Depends(get_db)) -> Mission:
    course = db.scalar(select(Course).where(Course.slug == slug))
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")

    mission = db.scalar(
        select(Mission)
        .join(Mission.sprint)
        .where(Mission.sprint.has(course_id=course.id), Mission.number == number)
    )
    if mission is None:
        raise HTTPException(status_code=404, detail="Mission not found")
    return mission
