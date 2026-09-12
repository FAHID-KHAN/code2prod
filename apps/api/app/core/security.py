"""Password hashing, opaque token generation, and JWT encode/decode.

Crypto primitives come from argon2-cffi, PyJWT and `secrets` — nothing here
implements its own (blueprint §17, §20).
"""

import hashlib
import secrets
import uuid
from datetime import UTC, datetime, timedelta
from typing import Any, Literal

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerifyMismatchError

from app.core.config import settings

_hasher = PasswordHasher()

# Verified against when no user matches, so a missing account costs the same time
# as a wrong password and cannot be detected by timing.
_DUMMY_HASH = _hasher.hash("timing-attack-placeholder")

TokenType = Literal["access"]


def hash_password(password: str) -> str:
    return _hasher.hash(password)


def verify_password(password: str, password_hash: str | None) -> bool:
    try:
        _hasher.verify(password_hash or _DUMMY_HASH, password)
    except (VerifyMismatchError, InvalidHashError):
        return False
    return True


def password_needs_rehash(password_hash: str) -> bool:
    return _hasher.check_needs_rehash(password_hash)


def generate_opaque_token() -> str:
    """A high-entropy token for refresh and one-time flows."""
    return secrets.token_urlsafe(48)


def hash_opaque_token(token: str) -> str:
    """Opaque tokens are stored hashed, so a database leak grants no sessions.

    SHA-256 is correct here rather than argon2: these are already 384 bits of
    CSPRNG output, so they are not brute-forceable and lookup must stay cheap.
    """
    return hashlib.sha256(token.encode()).hexdigest()


def create_access_token(user_id: int, role: str) -> tuple[str, datetime]:
    now = datetime.now(UTC)
    expires_at = now + timedelta(minutes=settings.access_token_ttl_minutes)
    payload: dict[str, Any] = {
        "sub": str(user_id),
        "role": role,
        "type": "access",
        "jti": uuid.uuid4().hex,
        "iat": int(now.timestamp()),
        "exp": int(expires_at.timestamp()),
    }
    token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
    return token, expires_at


def decode_access_token(token: str) -> dict[str, Any] | None:
    try:
        payload: dict[str, Any] = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
            options={"require": ["exp", "sub", "type"]},
        )
    except jwt.InvalidTokenError:
        return None

    if payload.get("type") != "access":
        return None
    return payload
