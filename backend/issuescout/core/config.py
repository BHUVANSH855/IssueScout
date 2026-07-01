from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "IssueScout"
    API_VERSION: str = "0.1.0"

    # GitHub configuration
    GITHUB_API: str = "https://api.github.com"
    GITHUB_TOKEN: str | None = None

    # Default repository
    DEFAULT_OWNER: str = "python"
    DEFAULT_REPOSITORY: str = "cpython"

    # CORS configuration
    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:5173",
    ]

    # HTTP client configuration
    REQUEST_TIMEOUT: int = 30
    MAX_PAGE_SIZE: int = 100
    MAX_CONCURRENT_REQUESTS: int = 10

    # Retry configuration
    GITHUB_MAX_RETRIES: int = 3
    GITHUB_RETRY_BACKOFF: float = 1.5

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()
