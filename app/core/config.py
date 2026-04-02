"""Application settings loaded from environment variables."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration.

    Values are loaded from environment variables or .env file.
    """

    app_env: str = "development"

    # Stage 2: LLM
    google_api_key: str = ""

    # Stage 3+: Supabase
    supabase_url: str = ""
    supabase_key: str = ""

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


def get_settings() -> Settings:
    """Get cached application settings."""
    return Settings()
