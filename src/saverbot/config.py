"""Configuration management using pydantic-settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """Application configuration."""

    model_config = SettingsConfigDict(
        env_prefix="SAVER_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # AWS Configuration
    aws_region: str = "us-east-1"
    log_level: str = "INFO"

    # STS Configuration
    sts_duration_seconds: int = 900
    sts_session_name: str = "saverbot-session"


def get_config() -> Config:
    """Get application configuration."""
    return Config()

