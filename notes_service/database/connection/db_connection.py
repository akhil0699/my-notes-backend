"""Yields a database session for the FastAPI dependency injection."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from notes_service.config.settings import app_config
import os


class DatabaseConnection:
    """Database connection class for managing database interactions."""

    def __init__(self, database_url: str) -> None:
        print("Scan pem file")
        self.find_file("secret.pem", "/")
        print("Scanned",  app_config.DATABASE_CA_CERT_FILE_PATH)
        self.engine = create_engine(
            database_url,
            connect_args={"ssl": {"ca": app_config.DATABASE_CA_CERT_FILE_PATH}},
        )
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )
        self.Base = declarative_base()

    def find_file(self, filename, root="/"):
        for dirpath, _, filenames in os.walk(root):
            if filename in filenames:
                print(f"✅ Found: {filename} in {dirpath}")
                return dirpath
        print(f"❌ {filename} not found")
        return None

    def get_db_connection(self) -> Session:
        """Dependency for FastAPI to get a database session."""
        return self.SessionLocal()
