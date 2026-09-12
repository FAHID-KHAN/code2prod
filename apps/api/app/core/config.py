from typing import Self

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

DEV_JWT_SECRET = "dev-only-insecure-secret-change-me"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+psycopg://code2prod:code2prod@localhost:5432/code2prod"
    environment: str = "development"

    jwt_secret: str = DEV_JWT_SECRET
    jwt_algorithm: str = "HS256"
    # Access tokens are verified without a database lookup, so they cannot be
    # revoked mid-life. This TTL is therefore the worst-case window between
    # revoking a session and it actually going dead — keep it short.
    access_token_ttl_minutes: int = 15
    refresh_token_ttl_days: int = 30

    email_verification_ttl_hours: int = 48
    password_reset_ttl_minutes: int = 60

    @property
    def is_production(self) -> bool:
        return self.environment == "production"

    @model_validator(mode="after")
    def _reject_dev_secret_outside_development(self) -> Self:
        if self.environment != "development" and self.jwt_secret == DEV_JWT_SECRET:
            raise ValueError(
                "JWT_SECRET must be set to a real value when ENVIRONMENT is not 'development'"
            )
        return self


settings = Settings()
