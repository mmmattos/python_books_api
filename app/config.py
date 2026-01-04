import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    env: str
    database_url: str
    debug: bool


def load_settings() -> Settings:
    return Settings(
        env=os.getenv("APP_ENV", "dev"),
        database_url=os.getenv(
            "DATABASE_URL",
            "file:books.db?cache=shared",
        ),
        debug=os.getenv("DEBUG", "false").lower() == "true",
    )


settings = load_settings()