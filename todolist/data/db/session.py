from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Optional

from todolist.config.settings import Settings

def get_engine(database_url: Optional[str]) -> Engine:
    """Get a SQLAlchemy engine for the given database URL."""
    if database_url is None:
        settings = Settings.load()
        if settings.DATABASE_URL is None:
            # Generate it
            database_url = f"postgresql+psycopg2://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
        else:
            database_url = settings.DATABASE_URL

    return create_engine(database_url)


def get_session_factory() -> sessionmaker:
    """Get a SQLAlchemy session factory for the given database URL."""
    engine = get_engine()
    return sessionmaker(bind=engine)
