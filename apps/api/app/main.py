from fastapi import FastAPI

from app.core.logging import configure_logging, register_exception_logging
from app.core.middleware import RequestLoggingMiddleware
from app.domains.auth.router import router as auth_router
from app.domains.courses.router import router as courses_router
from app.domains.health.router import router as health_router

configure_logging()

# Schema is applied by `alembic upgrade head`, never by the app at startup, so a
# rollout can never silently reshape the database.
app = FastAPI(title="Code2Prod API")
app.add_middleware(RequestLoggingMiddleware)
register_exception_logging(app)

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(courses_router)
