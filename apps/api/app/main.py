from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.db import Base, SessionLocal, engine
from app.domains.courses.router import router as courses_router
from app.domains.health.router import router as health_router
from app.seed.build_course import seed_build_course


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        seed_build_course(db)
    yield


app = FastAPI(title="Code2Prod API", lifespan=lifespan)
app.include_router(health_router)
app.include_router(courses_router)
