from __future__ import annotations

from datetime import date
from typing import Iterable, Optional, Union, Tuple, List

from todolist.config.settings import Settings
from todolist.core.domain.status import TaskStatus
from todolist.core.domain.task import Task
from todolist.core.domain.project import Project
from todolist.core.repositories.project_repository import ProjectRepository
from todolist.core.repositories.task_repository import TaskRepository

def can_cast_to_int(s: Union[str, int]) -> bool:
    try:
        int(s)
        return True
    except (ValueError, TypeError):
        return False


class TaskService:
    """Service for managing tasks whithin a project context."""
    
    def __init__(self, task_repo: TaskRepository, project_repo: ProjectRepository, settings: Settings) -> None:
        self.task_repo = task_repo
        self.project_repo = project_repo
        self.settings = settings
    
    def add_task(
        self,
        project_identifier: Union[str, int],
        *,
        name: str,
        description: str = "",
        status: TaskStatus = TaskStatus.TODO,
        deadline: Optional[date] = None
    ) -> Task:
        project: Project
        if can_cast_to_int(project_identifier):
            project = self.project_repo.get_by_id(int(project_identifier))
        else:
            project = self.project_repo.get_by_name(project_identifier)
        if project is None:
            raise ValueError("Project not found.")
        task_count: int = len(list(self.task_repo.list_by_project(project.id)))
        if task_count == self.settings.MAX_TASKS:
            raise ValueError("You have reached maximum number of tasks per project.")
        
        task = Task(
            project_id = project.id,
            name = name,
            description = description,
            status = status,
            deadline = deadline
        )
        return self.task_repo.add(task)
    
    def delete_task(self, task_id: int) -> bool:
        return self.task_repo.remove(task_id)
    
    def get_task(self, task_id: int) -> Optional[Task]:
        """Return a single task or None."""
        return self.task_repo.get_by_id(task_id)
    
    def list_tasks(
        self,
        *,
        skip: int = 0,
        limit: int = 20,
        status: Optional[TaskStatus] = None,
        search: Optional[str] = None,
        due_from: Optional[date] = None,
        due_to: Optional[date] = None,
        sort: Optional[str] = None,
    ) -> Tuple[List[Task], int]:
        """List tasks with basic filtering and pagination."""
        tasks: List[Task] = list(self.task_repo.list_all_tasks())

        if status:
            tasks = [task for task in tasks if task.status == status]
        if search:
            term = search.lower()
            tasks = [task for task in tasks if term in task.name.lower() or term in (task.description or "").lower()]
        if due_from:
            tasks = [task for task in tasks if task.deadline and task.deadline >= due_from]
        if due_to:
            tasks = [task for task in tasks if task.deadline and task.deadline <= due_to]

        tasks = self._sort_tasks(tasks, sort)

        total = len(tasks)
        if skip < 0:
            skip = 0
        if limit is None or limit < 0:
            limit = total
        tasks = tasks[skip : skip + limit]
        return tasks, total
    
    def list_tasks_by_project(self, project_identifier: Union[str, int]) -> Iterable[Task]:
        project: Project
        if can_cast_to_int(project_identifier):
            project = self.project_repo.get_by_id(int(project_identifier))
        else:
            project = self.project_repo.get_by_name(project_identifier)
        if project is None:
            raise ValueError("Project not found.")
        tasks: list = list(self.task_repo.list_by_project(project.id))
        return tasks
    
    def edit_task_name(self, task_id: int, *, name: str) -> Task:
        task: Task = self.task_repo.get_by_id(task_id)
        if task is None:
           raise ValueError("No Task found.")    
        if not name or len(name.strip()) == 0:
            raise ValueError("Task name cannot be empty")   
        if len(name) > self.settings.MAX_NAME_LEN:
            raise ValueError(f"Length of task name cannot be more than {self.settings.MAX_NAME_LEN} characters.")
        task.name = name
        return self.task_repo.update(task)
        
    def edit_task_description(self, task_id: int, *, description: str) -> Task:
        task: Task = self.task_repo.get_by_id(task_id)
        if task is None:
            raise ValueError("No Task found.")    
        if len(description) > self.settings.MAX_DESCRIPTION_LEN:
            raise ValueError(f"Length of task description cannot be more than {self.settings.MAX_DESCRIPTION_LEN} characters.")
        task.description = description            
        return self.task_repo.update(task)
        
    def edit_task_deadline(self, task_id: int, *, deadline: date) -> Task:
        task: Task = self.task_repo.get_by_id(task_id)
        if task is None:
            raise ValueError("No Task found.")            
        task.deadline = deadline           
        return self.task_repo.update(task)
    
    def _edit_task_closed_at(self, task_id: int, *, closed_at: Optional[date]) -> Task:
        task: Task = self.task_repo.get_by_id(task_id)
        if task is None:
            raise ValueError("No Task found.")            
        task.closed_at = closed_at           
        return self.task_repo.update(task)
        
    def change_status(self, task_id: int, status: TaskStatus) -> Task:
        task: Task = self.task_repo.get_by_id(task_id)
        if task is None:
            raise ValueError("No Task found.")            
        task.status = status
        return self.task_repo.update(task)

    def replace_task(
        self,
        task_id: int,
        *,
        name: str,
        description: Optional[str],
        status: TaskStatus,
        deadline: Optional[date],
        project_id: Optional[int] = None,
    ) -> Task:
        """Full replacement update akin to PUT."""
        task = self.task_repo.get_by_id(task_id)
        if task is None:
            raise ValueError("Task not found.")

        if project_id is not None:
            project = self.project_repo.get_by_id(project_id)
            if project is None:
                raise ValueError("Project not found.")
            task.project_id = project.id
        if not name or len(name.strip()) == 0:
            raise ValueError("Task name cannot be empty.")
        if len(name) > self.settings.MAX_NAME_LEN:
            raise ValueError(f"Length of task name cannot be more than {self.settings.MAX_NAME_LEN} characters.")
        if description is not None and len(description) > self.settings.MAX_DESCRIPTION_LEN:
            raise ValueError(
                f"Length of task description cannot be more than {self.settings.MAX_DESCRIPTION_LEN} characters."
            )

        task.name = name
        task.description = description or ""
        task.status = status
        task.deadline = deadline
        task.validate()
        return self.task_repo.update(task)

    def update_task_fields(
        self,
        task_id: int,
        *,
        name: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[TaskStatus] = None,
        deadline: Optional[date] = None,
        project_id: Optional[int] = None,
    ) -> Task:
        """Partial update akin to PATCH."""
        task = self.task_repo.get_by_id(task_id)
        if task is None:
            raise ValueError("Task not found.")

        if project_id is not None:
            project = self.project_repo.get_by_id(project_id)
            if project is None:
                raise ValueError("Project not found.")
            task.project_id = project.id

        if name is not None:
            if not name.strip():
                raise ValueError("Task name cannot be empty.")
            if len(name) > self.settings.MAX_NAME_LEN:
                raise ValueError(f"Length of task name cannot be more than {self.settings.MAX_NAME_LEN} characters.")
            task.name = name
        if description is not None:
            if len(description) > self.settings.MAX_DESCRIPTION_LEN:
                raise ValueError(
                    f"Length of task description cannot be more than {self.settings.MAX_DESCRIPTION_LEN} characters."
                )
            task.description = description
        if status is not None:
            task.status = status
        if deadline is not None:
            task.deadline = deadline

        task.validate()
        return self.task_repo.update(task)

    def toggle_completion(self, task_id: int) -> Task:
        """Flip status between DONE and TODO."""
        task = self.task_repo.get_by_id(task_id)
        if task is None:
            raise ValueError("Task not found.")
        task.status = TaskStatus.DONE if task.status != TaskStatus.DONE else TaskStatus.TODO
        return self.task_repo.update(task)

    @staticmethod
    def _sort_tasks(tasks: List[Task], sort: Optional[str]) -> List[Task]:
        """Sort tasks by supported fields."""
        if not sort:
            return sorted(tasks, key=lambda t: t.id or 0)
        descending = sort.startswith("-")
        key = sort.lstrip("-")
        if key == "deadline":
            return sorted(tasks, key=lambda t: t.deadline or date.max, reverse=descending)
        if key == "name":
            return sorted(tasks, key=lambda t: t.name.lower(), reverse=descending)
        if key == "status":
            return sorted(tasks, key=lambda t: t.status.value, reverse=descending)
        # default fallback
        return sorted(tasks, key=lambda t: t.id or 0, reverse=descending)
    
        