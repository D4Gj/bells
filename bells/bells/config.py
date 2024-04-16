import os
from pathlib import Path
from typing import Literal

from goodconf import Field, GoodConf

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bells.settings")

PROJECT_DIR = Path(__file__).parents[1].resolve()


class Config(GoodConf):
    """Configuration for bells"""

    DEBUG: bool = True
    ALLOWED_HOSTS: list[str] = Field(
        default=["*"],
        description="Hosts allowed to serve the site "
        "https://docs.djangoproject.com/en/5.0/ref/settings/#allowed-hosts",
    )
    DATABASE_URL: str = Field(
        default="sqlite:///./sqlite3.db",
        description="A string with the database URL as defined in "
        "https://github.com/jazzband/dj-database-url#url-schema",
    )
    DJANGO_ENV: Literal["development", "dev", "production"] = Field(
        default="dev",
        description="Toggle deployment settings for local development or production",
    )
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO",
        description="Python logging level",
    )
    SECRET_KEY: str = "dkfL7lxhP6y08FFe31V87Niwgv08gjYjk5DGHCjIk+Vygq4iuSitGhREuavr4LMCCOid6q9oeu3gfqnV"
    ENVIRONMENT: str = Field(
        "development",
        description="Name of deployed environment (e.g. 'staging', 'production')",
    )
    BASIC_AUTH_CREDENTIALS: str = Field(
        default="",
        description="Basic Auth credentials for the site in the format 'username:password'",
    )
    SENTRY_DSN: str = Field(
        default="",
        description="Sentry DSN to enable error logging",
    )
    SENTRY_TRACE_SAMPLE_RATE: float = Field(
        default=0.25,
        description="Sentry trace sample rate "
        "https://docs.sentry.io/product/sentry-basics/concepts/tracing/trace-view/",
    )

    class Config:
        default_files = ["bells.yml"]


config = Config()
