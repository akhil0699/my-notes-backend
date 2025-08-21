"""Module of settings."""

from pathlib import Path
from pydantic_settings import BaseSettings


class AppConfig(BaseSettings):
    DATABASE_URL: str = "mysql+pymysql://avnadmin:AVNS_-3oMhPUnpnpqZeh0-le@mysql-a35ba9b-akhilinthehome6-24a4.f.aivencloud.com:16017/notes_akhil"
    ALLOW_ORIGINS: str = "*"
    ALLOW_CREDENTIALS: bool = True
    APP_URL: str = "https://my-notes-backend-t5xa.onrender.com"
    DATABASE_CA_CERT_FILE_PATH: str 

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


env_file_path = Path(__file__).parent.parent.resolve() / ".env"
app_config = AppConfig(
    _env_file=f"{env_file_path}",  # type: ignore
    _env_file_encoding="utf-8",
)
