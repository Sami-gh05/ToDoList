"""Application entry point for the ToDoList CLI (Phase 1).

Wires configuration, repositories, services, and starts a minimal CLI menu.
"""
from __future__ import annotations

from todolist.cli.menu import run_menu
from todolist.config.settings import Settings
from todolist.data.db.session import get_session_factory
from todolist.core.services.project_service import ProjectService
from todolist.core.services.task_service import TaskService
from todolist.core.services.schedular_service import SchedulerService
from todolist.data.repositories.SQL_DB_project_repository import SQL_DB_ProjectRepository
from todolist.data.repositories.SQL_DB_task_repository import SQL_DB_TaskRepository

def main() -> None:
    """Initialize application components and run the CLI."""
    settings = Settings.load()
    
    session_factory = get_session_factory(settings.DATABASE_URL)
    session = session_factory()

    project_repo = SQL_DB_ProjectRepository(session)
    task_repo = SQL_DB_TaskRepository(session)

    project_service = ProjectService(project_repo, task_repo, settings=settings)
    task_service = TaskService(task_repo, project_repo, settings=settings)


    scheduler = SchedulerService(task_repo)
    scheduler.start()
    
    try:
        print("ToDoList CLI (Phase 2 - PostgreSQL Backend)")
        run_menu(project_service, task_service)
    finally:
        # Stop scheduler when app exits
        scheduler.stop()


if __name__ == "__main__":
    main()


