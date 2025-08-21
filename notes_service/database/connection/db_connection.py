"""Yields a database session for the FastAPI dependency injection."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session


class DatabaseConnection:
    """Database connection class for managing database interactions."""

    def __init__(self, database_url: str) -> None:
        self.engine = create_engine(
            database_url,
            connect_args={"ssl": {"ca": "/home/calance/Downloads/ca.pem"}},
        )
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )
        self.Base = declarative_base()

    def get_db_connection(self) -> Session:
        """Dependency for FastAPI to get a database session."""
        return self.SessionLocal()
