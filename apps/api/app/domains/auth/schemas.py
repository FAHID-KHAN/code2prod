from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.domains.auth.models import Role


class RegisterRequest(BaseModel):
    email: EmailStr
    # Length is the property that actually matters; composition rules push users
    # toward predictable substitutions. NIST SP 800-63B guidance.
    password: str = Field(min_length=10, max_length=128)
    display_name: str = Field(min_length=1, max_length=100)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(max_length=128)


class TokenPair(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_at: datetime


class VerifyEmailRequest(BaseModel):
    token: str


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    token: str
    password: str = Field(min_length=10, max_length=128)


class ProfileOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    display_name: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    role: Role
    is_active: bool
    email_verified_at: datetime | None
    profile: ProfileOut | None


class MessageOut(BaseModel):
    detail: str
