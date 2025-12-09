from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Optional

from todolist.config.settings import Settings

Base = declarative_base()

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


def get_session_factory(database_url: Optional[str]) -> sessionmaker:
    """Get a SQLAlchemy session factory for the given database URL."""
    engine = get_engine(database_url)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)
