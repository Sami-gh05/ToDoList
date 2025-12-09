from __future__ import annotations

from typing import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from todolist.config.settings import Settings
from todolist.core.services.project_service import ProjectService
from todolist.core.services.task_service import TaskService
from todolist.data.db.session import get_session_factory
from todolist.data.repositories.SQL_DB_project_repository import SQL_DB_ProjectRepository
from todolist.data.repositories.SQL_DB_task_repository import SQL_DB_TaskRepository


settings = Settings.load()
SessionLocal = get_session_factory(settings.DATABASE_URL)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_project_service(db: Session = Depends(get_db)) -> ProjectService:
    project_repo = SQL_DB_ProjectRepository(db)
    task_repo = SQL_DB_TaskRepository(db)
    return ProjectService(project_repo, task_repo, settings=settings)


def get_task_service(db: Session = Depends(get_db)) -> TaskService:
    project_repo = SQL_DB_ProjectRepository(db)
    task_repo = SQL_DB_TaskRepository(db)
    return TaskService(task_repo, project_repo, settings=settings)

