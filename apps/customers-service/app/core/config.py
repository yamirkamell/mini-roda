"""Application configuration settings."""

import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    database_url: str = os.environ["ENV_CUSTOMERS_DATABASE_URL"]
    
    # API
    api_title: str = "Customers Service"
    api_version: str = "1.0.0"
    api_description: str = "API service for managing customers"
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8001
    
    # CORS
    cors_origins: list[str] = ["*"]
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        # Map environment variables (UPPER_SNAKE_CASE) to field names (snake_case)
        env_prefix="",
    )
    
    @classmethod
    def from_env(cls) -> "Settings":
        """Create settings from environment variables."""
        return cls()


settings = Settings()

