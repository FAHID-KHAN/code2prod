import httpx
from fastapi.testclient import TestClient
from sqlalchemy import select

from app.core.db import SessionLocal
from app.domains.auth.models import OneTimeToken, Role, User
from app.domains.auth.router import REFRESH_COOKIE
from app.main import app
from tests.conftest import Outbox

PASSWORD = "correct-horse-battery"


def _token_from(outbox: Outbox) -> str:
    """Recover the token a user would have received, from the most recent email."""
    for message in reversed(outbox):
        if "token: " in message["body"]:
            return message["body"].split("token: ", 1)[1].strip()
    raise AssertionError(f"no token found in outbox: {outbox}")


def _refresh_from_other_client(token: str) -> httpx.Response:
    """Present a refresh token from a client holding no cookies.

    The endpoint prefers the cookie over the header, so reusing the logged-in
    client here would silently exercise its own valid cookie instead of `token`.
    A separate client is also the honest simulation of a stolen credential.
    """
    with TestClient(app) as attacker:
        return attacker.post("/auth/refresh", headers={"x-refresh-token": token})


def register(client: TestClient, email: str, display_name: str = "Test Learner") -> httpx.Response:
    return client.post(
        "/auth/register",
        json={"email": email, "password": PASSWORD, "display_name": display_name},
    )


def register_and_verify(client: TestClient, email: str, outbox: Outbox) -> None:
    assert register(client, email).status_code == 202
    token = _token_from(outbox)
    assert client.post("/auth/verify-email", json={"token": token}).status_code == 200


def test_register_creates_unverified_user(client: TestClient, outbox: Outbox) -> None:
    email = "new.learner@example.com"
    assert register(client, email, display_name="New Learner").status_code == 202

    with SessionLocal() as db:
        user = db.scalar(select(User).where(User.email == email))
        assert user is not None
        assert user.email_verified_at is None
        assert user.role is Role.STUDENT
        assert user.password_hash != PASSWORD
        assert user.profile.display_name == "New Learner"


def test_register_sends_a_verification_email(client: TestClient, outbox: Outbox) -> None:
    email = "mailed@example.com"
    register(client, email)

    assert len(outbox) == 1
    assert outbox[0]["to"] == email
    assert _token_from(outbox)


def test_register_normalizes_email_case(client: TestClient, outbox: Outbox) -> None:
    register(client, "MiXeD@Example.COM", display_name="Case")

    with SessionLocal() as db:
        assert db.scalar(select(User).where(User.email == "mixed@example.com")) is not None


def test_register_does_not_leak_existing_accounts(client: TestClient, outbox: Outbox) -> None:
    email = "duplicate@example.com"

    first = register(client, email)
    second = register(client, email)

    # Identical response either way, and no second account.
    assert first.status_code == second.status_code == 202
    assert first.json() == second.json()

    with SessionLocal() as db:
        assert len(list(db.scalars(select(User).where(User.email == email)))) == 1

    # The real owner is warned, but the caller learns nothing.
    assert "already exists" in outbox[-1]["body"]


def test_login_requires_verified_email(client: TestClient, outbox: Outbox) -> None:
    email = "unverified@example.com"
    register(client, email)

    response = client.post("/auth/login", json={"email": email, "password": PASSWORD})
    assert response.status_code == 403


def test_full_login_flow_returns_access_and_refresh(client: TestClient, outbox: Outbox) -> None:
    email = "verified@example.com"
    register_and_verify(client, email, outbox)

    response = client.post("/auth/login", json={"email": email, "password": PASSWORD})
    assert response.status_code == 200

    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]
    assert REFRESH_COOKIE in response.cookies

    me = client.get("/auth/me", headers={"Authorization": f"Bearer {body['access_token']}"})
    assert me.status_code == 200
    assert me.json()["email"] == email


def test_login_with_wrong_password_is_rejected(client: TestClient, outbox: Outbox) -> None:
    email = "wrongpass@example.com"
    register_and_verify(client, email, outbox)

    response = client.post("/auth/login", json={"email": email, "password": "not-the-password"})
    assert response.status_code == 401


def test_unknown_email_and_wrong_password_are_indistinguishable(
    client: TestClient, outbox: Outbox
) -> None:
    email = "known@example.com"
    register_and_verify(client, email, outbox)

    wrong = client.post("/auth/login", json={"email": email, "password": "not-the-password"})
    missing = client.post(
        "/auth/login", json={"email": "nobody@example.com", "password": PASSWORD}
    )

    assert wrong.status_code == missing.status_code == 401
    assert wrong.json() == missing.json()


def test_me_rejects_missing_and_malformed_tokens(client: TestClient) -> None:
    assert client.get("/auth/me").status_code == 401
    assert client.get("/auth/me", headers={"Authorization": "Bearer nonsense"}).status_code == 401


def test_refresh_rotates_and_supersedes_the_old_token(
    client: TestClient, outbox: Outbox
) -> None:
    email = "rotation@example.com"
    register_and_verify(client, email, outbox)
    client.post("/auth/login", json={"email": email, "password": PASSWORD})

    original = client.cookies[REFRESH_COOKIE]
    assert client.post("/auth/refresh").status_code == 200
    assert client.cookies[REFRESH_COOKIE] != original

    # The superseded token no longer works.
    assert _refresh_from_other_client(original).status_code == 401


def test_refresh_reuse_revokes_entire_family(client: TestClient, outbox: Outbox) -> None:
    email = "reuse@example.com"
    register_and_verify(client, email, outbox)
    client.post("/auth/login", json={"email": email, "password": PASSWORD})

    stolen = client.cookies[REFRESH_COOKIE]
    client.post("/auth/refresh")
    legitimate = client.cookies[REFRESH_COOKIE]

    # Replaying the rotated-away token is the signal that the chain leaked.
    assert _refresh_from_other_client(stolen).status_code == 401

    # The honest holder's still-current token dies with the family.
    assert _refresh_from_other_client(legitimate).status_code == 401


def test_logout_revokes_refresh_token(client: TestClient, outbox: Outbox) -> None:
    email = "logout@example.com"
    register_and_verify(client, email, outbox)
    client.post("/auth/login", json={"email": email, "password": PASSWORD})
    token = client.cookies[REFRESH_COOKIE]

    assert client.post("/auth/logout").status_code == 200
    assert _refresh_from_other_client(token).status_code == 401


def test_password_reset_rotates_password_and_kills_sessions(
    client: TestClient, outbox: Outbox
) -> None:
    email = "reset@example.com"
    register_and_verify(client, email, outbox)
    client.post("/auth/login", json={"email": email, "password": PASSWORD})
    old_refresh = client.cookies[REFRESH_COOKIE]

    assert client.post("/auth/password-reset/request", json={"email": email}).status_code == 202
    reset_token = _token_from(outbox)

    new_password = "a-brand-new-passphrase"
    confirm = client.post(
        "/auth/password-reset/confirm", json={"token": reset_token, "password": new_password}
    )
    assert confirm.status_code == 200

    # Old credentials and every old session are dead; the new password works.
    stale = client.post("/auth/login", json={"email": email, "password": PASSWORD})
    assert stale.status_code == 401
    assert _refresh_from_other_client(old_refresh).status_code == 401

    fresh = client.post("/auth/login", json={"email": email, "password": new_password})
    assert fresh.status_code == 200


def test_password_reset_for_unknown_email_is_silent(client: TestClient, outbox: Outbox) -> None:
    response = client.post("/auth/password-reset/request", json={"email": "ghost@example.com"})

    assert response.status_code == 202
    assert outbox == []


def test_one_time_token_cannot_be_replayed(client: TestClient, outbox: Outbox) -> None:
    register(client, "replay@example.com", display_name="Replay")
    token = _token_from(outbox)

    assert client.post("/auth/verify-email", json={"token": token}).status_code == 200
    assert client.post("/auth/verify-email", json={"token": token}).status_code == 400


def test_tokens_are_never_stored_in_plaintext(client: TestClient, outbox: Outbox) -> None:
    register(client, "hashed@example.com", display_name="Hashed")
    token = _token_from(outbox)

    with SessionLocal() as db:
        stored = list(db.scalars(select(OneTimeToken.token_hash)))
    assert token not in stored


def test_short_password_is_rejected(client: TestClient) -> None:
    response = client.post(
        "/auth/register",
        json={"email": "short@example.com", "password": "tiny", "display_name": "Short"},
    )
    assert response.status_code == 422


def test_rate_limit_blocks_login_brute_force(client: TestClient, outbox: Outbox) -> None:
    email = "brute@example.com"
    register_and_verify(client, email, outbox)

    statuses = [
        client.post("/auth/login", json={"email": email, "password": "wrong"}).status_code
        for _ in range(12)
    ]
    assert 429 in statuses
