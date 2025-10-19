"""Application entry point for the ToDoList CLI (Phase 1).

Wires configuration, repositories, services, and starts a minimal CLI menu.
"""
from __future__ import annotations

from todolist.cli.menu import run_menu
from todolist.config.settings import Settings
from todolist.core.services.project_service import ProjectService
from todolist.core.services.task_service import TaskService
from todolist.data.repositories.in_memory_project_repository import InMemoryProjectRepository
from todolist.data.repositories.in_memory_task_repository import InMemoryTaskRepository


def main() -> None:
    """Initialize application components and run the CLI."""
    settings = Settings.load()

    project_repo = InMemoryProjectRepository()
    task_repo = InMemoryTaskRepository()

    project_service = ProjectService(project_repo, task_repo, settings=settings)
    task_service = TaskService(task_repo, project_repo, settings=settings)

    print("ToDoList CLI (Phase 1 - In-Memory)")
    run_menu(project_service, task_service)


if __name__ == "__main__":
    main()


