"""Module of settings."""

from pathlib import Path
from pydantic_settings import BaseSettings


class AppConfig(BaseSettings):
    DATABASE_URL: str
    ALLOW_ORIGINS: str = "*"
    ALLOW_CREDENTIALS: bool = True
    APP_URL: str = "http://localhost:8001"
    DATABASE_CA_CERT_FILE_PATH: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


env_file_path = Path(__file__).parent.parent.resolve() / ".env"
app_config = AppConfig(
    _env_file=f"{env_file_path}",  # type: ignore
    _env_file_encoding="utf-8",
)
