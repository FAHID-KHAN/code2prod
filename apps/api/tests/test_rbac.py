"""Authorisation is enforced in the API, not just hidden in the UI (§20).

`require_role` has no product caller yet — the admin surface arrives in Phase 2 —
so it is exercised here against a throwaway app rather than left untested.
"""

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import select

from app.core.db import SessionLocal
from app.domains.auth.dependencies import require_role
from app.domains.auth.models import Role, User
from tests.conftest import Outbox
from tests.test_auth import PASSWORD, register_and_verify

rbac_app = FastAPI()


@rbac_app.get(
    "/admin-only", dependencies=[Depends(require_role(Role.ADMIN, Role.SUPER_ADMIN))]
)
def _admin_only() -> dict[str, bool]:
    return {"ok": True}


def _access_token(client: TestClient, email: str, outbox: Outbox) -> str:
    register_and_verify(client, email, outbox)
    response = client.post("/auth/login", json={"email": email, "password": PASSWORD})
    assert response.status_code == 200
    token: str = response.json()["access_token"]
    return token


def _promote(email: str, role: Role) -> None:
    with SessionLocal() as db:
        user = db.scalar(select(User).where(User.email == email))
        assert user is not None
        user.role = role
        db.commit()


def test_student_is_denied_an_admin_endpoint(client: TestClient, outbox: Outbox) -> None:
    token = _access_token(client, "student-rbac@example.com", outbox)

    with TestClient(rbac_app) as rbac_client:
        response = rbac_client.get("/admin-only", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 403


def test_admin_is_allowed(client: TestClient, outbox: Outbox) -> None:
    email = "admin-rbac@example.com"
    token = _access_token(client, email, outbox)
    _promote(email, Role.ADMIN)

    with TestClient(rbac_app) as rbac_client:
        response = rbac_client.get("/admin-only", headers={"Authorization": f"Bearer {token}"})

    # The same token now passes: the role is read from the database per request
    # rather than trusted from the token, so a change takes effect immediately.
    assert response.status_code == 200


def test_demotion_takes_effect_without_waiting_for_expiry(
    client: TestClient, outbox: Outbox
) -> None:
    email = "demoted-rbac@example.com"
    token = _access_token(client, email, outbox)
    _promote(email, Role.ADMIN)
    headers = {"Authorization": f"Bearer {token}"}

    with TestClient(rbac_app) as rbac_client:
        assert rbac_client.get("/admin-only", headers=headers).status_code == 200
        _promote(email, Role.STUDENT)
        assert rbac_client.get("/admin-only", headers=headers).status_code == 403


def test_deactivated_user_is_rejected(client: TestClient, outbox: Outbox) -> None:
    email = "deactivated-rbac@example.com"
    token = _access_token(client, email, outbox)

    with SessionLocal() as db:
        user = db.scalar(select(User).where(User.email == email))
        assert user is not None
        user.is_active = False
        db.commit()

    with TestClient(rbac_app) as rbac_client:
        response = rbac_client.get("/admin-only", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 401


def test_endpoint_requires_authentication(client: TestClient) -> None:
    with TestClient(rbac_app) as rbac_client:
        assert rbac_client.get("/admin-only").status_code == 401
