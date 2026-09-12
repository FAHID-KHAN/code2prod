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
from app.core.rate_limit import limiter  # noqa: E402
from app.main import app  # noqa: E402
from app.seed.build_course import seed_build_course  # noqa: E402

_API_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

Outbox = list[dict[str, str]]


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


@pytest.fixture(autouse=True)
def _clear_rate_limits() -> Iterator[None]:
    # Limits are per-process; without this the suite trips its own throttles.
    limiter.reset()
    yield
    limiter.reset()


@pytest.fixture
def outbox(monkeypatch: pytest.MonkeyPatch) -> Outbox:
    """Collect the emails the service sends.

    Asserting on an outbox rather than scraping log output keeps tests
    independent of the logging format, and will keep working unchanged once a
    real provider replaces the console sender.
    """
    sent: Outbox = []

    def fake_send(to: str, subject: str, body: str) -> None:
        sent.append({"to": to, "subject": subject, "body": body})

    monkeypatch.setattr("app.domains.auth.service.send_email", fake_send)
    return sent
