from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+psycopg://code2prod:code2prod@localhost:5432/code2prod"
    environment: str = "development"


settings = Settings()
