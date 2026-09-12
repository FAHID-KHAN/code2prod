from pydantic import BaseModel, ConfigDict


class MissionSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    number: int
    title: str
    mission_type: str


class MissionDetail(MissionSummary):
    context: str | None
    ticket: str | None
    acceptance_criteria: list[str] | None
    submission_type: str | None


class SprintSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    order: int
    missions: list[MissionSummary]


class CourseSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    slug: str
    name: str
    role: str
    is_free: bool
    price_bdt_min: int | None
    price_bdt_max: int | None


class CourseDetail(CourseSummary):
    sprints: list[SprintSummary]
