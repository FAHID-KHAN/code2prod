import os
import tempfile
from collections.abc import Iterator

import pytest

_db_fd, _db_path = tempfile.mkstemp(suffix=".sqlite3")
os.environ["DATABASE_URL"] = f"sqlite:///{_db_path}"

# Imported after DATABASE_URL is set: app.core.config builds its Settings at import time.
from alembic import command  # noqa: E402
from alembic.config import Config  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from app.core.db import SessionLocal  # noqa: E402
from app.main import app  # noqa: E402
from app.seed.build_course import seed_build_course  # noqa: E402

_API_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture(scope="session", autouse=True)
def _database() -> Iterator[None]:
    # Building the schema from migrations rather than metadata means a broken or
    # missing migration fails the test suite, not production.
    config = Config(os.path.join(_API_ROOT, "alembic.ini"))
    config.set_main_option("script_location", os.path.join(_API_ROOT, "migrations"))
    command.upgrade(config, "head")

    with SessionLocal() as db:
        seed_build_course(db)

    yield

    os.close(_db_fd)
    os.remove(_db_path)


@pytest.fixture(scope="session")
def client() -> Iterator[TestClient]:
    with TestClient(app) as test_client:
        yield test_client
