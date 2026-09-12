import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class Role(str, enum.Enum):
    STUDENT = "student"
    MENTOR = "mentor"
    REVIEWER = "reviewer"
    SUPPORT_AGENT = "support_agent"
    CONTENT_CREATOR = "content_creator"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"


class TokenPurpose(str, enum.Enum):
    EMAIL_VERIFICATION = "email_verification"
    PASSWORD_RESET = "password_reset"


def _utcnow_column() -> Mapped[datetime]:
    # current_timestamp() rather than now(): identical on PostgreSQL, but it also
    # compiles on SQLite, which the test database uses.
    return mapped_column(DateTime(timezone=True), server_default=func.current_timestamp())


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    # Stored lower-cased so uniqueness is case-insensitive without a citext extension.
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[Role] = mapped_column(
        Enum(Role, name="user_role", values_callable=lambda e: [m.value for m in e]),
        default=Role.STUDENT,
    )
    is_active: Mapped[bool] = mapped_column(default=True)
    email_verified_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), default=None
    )
    created_at: Mapped[datetime] = _utcnow_column()
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )

    profile: Mapped["Profile"] = relationship(
        back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    refresh_tokens: Mapped[list["RefreshToken"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    @property
    def is_verified(self) -> bool:
        return self.email_verified_at is not None


class Profile(Base):
    __tablename__ = "profiles"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    display_name: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = _utcnow_column()

    user: Mapped[User] = relationship(back_populates="profile")


class RefreshToken(Base):
    """One link in a rotating refresh-token chain.

    Each login starts a family. Every refresh revokes the presented token and
    issues a successor in the same family, so presenting an already-revoked token
    means it leaked — the whole family is then killed (see auth.service).
    """

    __tablename__ = "refresh_tokens"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    token_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    family_id: Mapped[str] = mapped_column(String(32), index=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
    created_at: Mapped[datetime] = _utcnow_column()

    user: Mapped[User] = relationship(back_populates="refresh_tokens")


class OneTimeToken(Base):
    """Single-use token for email verification and password reset."""

    __tablename__ = "one_time_tokens"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    token_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    purpose: Mapped[TokenPurpose] = mapped_column(
        Enum(TokenPurpose, name="token_purpose", values_callable=lambda e: [m.value for m in e])
    )
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
    created_at: Mapped[datetime] = _utcnow_column()
