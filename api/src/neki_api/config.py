from typing import Literal, Self
from urllib.parse import urlsplit

from pydantic import Field, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import make_url


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="NEKI_", extra="forbid", hide_input_in_errors=True)

    environment: Literal["local", "test", "staging", "production"] = "local"
    database_url: SecretStr
    database_timeout_seconds: float = Field(default=3, ge=0.1, le=10)
    pool_size: int = Field(default=5, ge=1, le=20)
    allowed_origins: list[str] = []
    sms_provider: Literal["disabled", "test", "msg91"] = "disabled"
    payments_enabled: Literal[False] = False

    @model_validator(mode="after")
    def validate_boundaries(self) -> Self:
        try:
            url = make_url(self.database_url.get_secret_value())
        except Exception:
            raise ValueError("Database URL must be a valid PostgreSQL URL") from None
        if url.drivername != "postgresql+psycopg" or not url.database:
            raise ValueError("Use a named PostgreSQL database with postgresql+psycopg")
        remote = self.environment in {"staging", "production"}
        if remote and (not url.password or url.query.get("sslmode") != "verify-full"):
            raise ValueError(
                "Deployed database connections require credentials and verify-full TLS"
            )
        if remote and self.sms_provider == "test":
            raise ValueError("The test SMS provider is forbidden outside local/test")
        for origin in self.allowed_origins:
            parsed = urlsplit(origin)
            if (
                parsed.scheme not in {"http", "https"}
                or not parsed.hostname
                or parsed.username
                or parsed.password
                or parsed.path
                or parsed.query
                or parsed.fragment
                or (remote and parsed.scheme != "https")
                or "*" in origin
            ):
                raise ValueError(
                    "Allowed origins must be exact origins; deployed origins require HTTPS"
                )
        return self
