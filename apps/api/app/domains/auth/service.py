"""Auth business logic.

Two rules shape most of this:

1. Endpoints must not reveal whether an email address has an account, so
   registration and password-reset requests succeed identically either way.
2. Anything handed to a user is stored hashed, never in plaintext.
"""

import logging
import uuid
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.email import send_email
from app.core.security import (
    create_access_token,
    generate_opaque_token,
    hash_opaque_token,
    hash_password,
    password_needs_rehash,
    verify_password,
)
from app.domains.auth.models import OneTimeToken, Profile, RefreshToken, Role, TokenPurpose, User

logger = logging.getLogger("app.auth")


class AuthError(Exception):
    """Raised for any credential or token failure the client may see."""

    def __init__(self, detail: str, status_code: int = 401) -> None:
        super().__init__(detail)
        self.detail = detail
        self.status_code = status_code


@dataclass(frozen=True)
class IssuedTokens:
    access_token: str
    access_expires_at: datetime
    refresh_token: str
    refresh_expires_at: datetime


def _as_utc(value: datetime) -> datetime:
    """Treat a stored timestamp as UTC-aware.

    Everything is written as UTC, but not every backend hands it back with a
    timezone attached — PostgreSQL does, SQLite does not. Normalising on read
    keeps expiry comparisons correct on both.
    """
    return value if value.tzinfo is not None else value.replace(tzinfo=UTC)


def normalize_email(email: str) -> str:
    return email.strip().lower()


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.scalar(select(User).where(User.email == normalize_email(email)))


def _issue_one_time_token(
    db: Session, user: User, purpose: TokenPurpose, ttl: timedelta
) -> str:
    token = generate_opaque_token()
    db.add(
        OneTimeToken(
            user_id=user.id,
            token_hash=hash_opaque_token(token),
            purpose=purpose,
            expires_at=datetime.now(UTC) + ttl,
        )
    )
    return token


def _consume_one_time_token(db: Session, token: str, purpose: TokenPurpose) -> User:
    record = db.scalar(
        select(OneTimeToken).where(
            OneTimeToken.token_hash == hash_opaque_token(token),
            OneTimeToken.purpose == purpose,
        )
    )
    now = datetime.now(UTC)

    if record is None or record.used_at is not None or _as_utc(record.expires_at) <= now:
        raise AuthError("Invalid or expired token", status_code=400)

    record.used_at = now
    user = db.get(User, record.user_id)
    if user is None:
        raise AuthError("Invalid or expired token", status_code=400)
    return user


def _issue_refresh_token(db: Session, user: User, family_id: str) -> tuple[str, datetime]:
    token = generate_opaque_token()
    expires_at = datetime.now(UTC) + timedelta(days=settings.refresh_token_ttl_days)
    db.add(
        RefreshToken(
            user_id=user.id,
            token_hash=hash_opaque_token(token),
            family_id=family_id,
            expires_at=expires_at,
        )
    )
    return token, expires_at


def _issue_tokens(db: Session, user: User, family_id: str) -> IssuedTokens:
    access_token, access_expires_at = create_access_token(user.id, user.role.value)
    refresh_token, refresh_expires_at = _issue_refresh_token(db, user, family_id)
    return IssuedTokens(
        access_token=access_token,
        access_expires_at=access_expires_at,
        refresh_token=refresh_token,
        refresh_expires_at=refresh_expires_at,
    )


def _revoke_family(db: Session, family_id: str) -> None:
    now = datetime.now(UTC)
    tokens = db.scalars(
        select(RefreshToken).where(
            RefreshToken.family_id == family_id, RefreshToken.revoked_at.is_(None)
        )
    )
    for token in tokens:
        token.revoked_at = now


def revoke_all_sessions(db: Session, user: User) -> None:
    now = datetime.now(UTC)
    tokens = db.scalars(
        select(RefreshToken).where(
            RefreshToken.user_id == user.id, RefreshToken.revoked_at.is_(None)
        )
    )
    for token in tokens:
        token.revoked_at = now


def register(db: Session, email: str, password: str, display_name: str) -> None:
    normalized = normalize_email(email)
    existing = get_user_by_email(db, normalized)

    if existing is not None:
        # Do not disclose that the address is taken. Tell the real owner instead.
        send_email(
            to=normalized,
            subject="Someone tried to register with your email",
            body=(
                "An account already exists for this address. "
                "Reset your password if this wasn't you."
            ),
        )
        db.commit()
        return

    user = User(
        email=normalized,
        password_hash=hash_password(password),
        role=Role.STUDENT,
    )
    user.profile = Profile(display_name=display_name.strip())
    db.add(user)
    db.flush()

    token = _issue_one_time_token(
        db,
        user,
        TokenPurpose.EMAIL_VERIFICATION,
        timedelta(hours=settings.email_verification_ttl_hours),
    )
    send_email(
        to=normalized,
        subject="Verify your Code2Prod email",
        body=f"Verification token: {token}",
    )
    db.commit()
    logger.info("user registered", extra={"user_id": user.id})


def verify_email(db: Session, token: str) -> None:
    user = _consume_one_time_token(db, token, TokenPurpose.EMAIL_VERIFICATION)
    if user.email_verified_at is None:
        user.email_verified_at = datetime.now(UTC)
    db.commit()
    logger.info("email verified", extra={"user_id": user.id})


def login(db: Session, email: str, password: str) -> IssuedTokens:
    user = get_user_by_email(db, email)

    # Always run a verification so a missing account and a wrong password take
    # the same time; verify_password substitutes a dummy hash when user is None.
    password_ok = verify_password(password, user.password_hash if user else None)

    if user is None or not password_ok:
        raise AuthError("Incorrect email or password")
    if not user.is_active:
        raise AuthError("Account is disabled", status_code=403)
    if not user.is_verified:
        raise AuthError("Email address is not verified", status_code=403)

    if password_needs_rehash(user.password_hash):
        user.password_hash = hash_password(password)

    tokens = _issue_tokens(db, user, family_id=uuid.uuid4().hex)
    db.commit()
    logger.info("login succeeded", extra={"user_id": user.id})
    return tokens


def refresh(db: Session, refresh_token: str) -> IssuedTokens:
    record = db.scalar(
        select(RefreshToken).where(RefreshToken.token_hash == hash_opaque_token(refresh_token))
    )
    if record is None:
        raise AuthError("Invalid refresh token")

    if record.revoked_at is not None:
        # A revoked token was replayed: it was rotated away or stolen. Either way
        # the chain is no longer trustworthy, so kill every session in the family.
        _revoke_family(db, record.family_id)
        db.commit()
        logger.warning(
            "refresh token reuse detected",
            extra={"user_id": record.user_id, "family_id": record.family_id},
        )
        raise AuthError("Invalid refresh token")

    if _as_utc(record.expires_at) <= datetime.now(UTC):
        raise AuthError("Refresh token has expired")

    user = db.get(User, record.user_id)
    if user is None or not user.is_active:
        raise AuthError("Account is disabled", status_code=403)

    record.revoked_at = datetime.now(UTC)
    tokens = _issue_tokens(db, user, family_id=record.family_id)
    db.commit()
    return tokens


def logout(db: Session, refresh_token: str) -> None:
    record = db.scalar(
        select(RefreshToken).where(RefreshToken.token_hash == hash_opaque_token(refresh_token))
    )
    if record is not None:
        _revoke_family(db, record.family_id)
        db.commit()


def request_password_reset(db: Session, email: str) -> None:
    user = get_user_by_email(db, email)

    # Silent success for unknown addresses keeps this from being an oracle.
    if user is not None:
        token = _issue_one_time_token(
            db,
            user,
            TokenPurpose.PASSWORD_RESET,
            timedelta(minutes=settings.password_reset_ttl_minutes),
        )
        send_email(
            to=user.email,
            subject="Reset your Code2Prod password",
            body=f"Password reset token: {token}",
        )
        db.commit()


def confirm_password_reset(db: Session, token: str, password: str) -> None:
    user = _consume_one_time_token(db, token, TokenPurpose.PASSWORD_RESET)
    user.password_hash = hash_password(password)

    # A reset is the remedy for a compromised account, so every existing session
    # must die with it — including any the attacker holds.
    revoke_all_sessions(db, user)

    # Completing a reset proves control of the mailbox.
    if user.email_verified_at is None:
        user.email_verified_at = datetime.now(UTC)

    db.commit()
    logger.info("password reset completed", extra={"user_id": user.id})
