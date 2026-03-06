from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Mock API"
    app_version: str = "1.0.0"
    environment: str = "development"
    api_prefix: str = "/api/v1"

    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = False
    docs_enabled: bool = True

    log_level: str = "INFO"
    log_json: bool = True

    database_url: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/mock_api"
    )

    otel_enabled: bool = False
    otel_service_name: str = "mock-api"
    otel_exporter_otlp_endpoint: str = "http://localhost:4318"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
