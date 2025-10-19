from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Iterable, Optional

from todolist.config.settings import Settings
from todolist.core.domain.status import TaskStatus
from todolist.core.domain.task import Task
from todolist.core.repositories.project_repository import ProjectRepository
from todolist.core.repositories.task_repository import TaskRepository

@dataclass
class TaskService:
    """Service for managing tasks whithin a project context."""
    
    task_repo: TaskRepository
    project_repo: ProjectRepository
    settings: Settings
    
    def add_task(
        self,
        project_id: int,
        *,
        name: str,
        description: str = "",
        status: TaskStatus = TaskStatus.TODO,
        deadline: Optional[date] = None
    ) -> Task:
        if self.project_repo.get_by_id(project_id) is None:
            raise ValueError("Project not found.")
        task_count: int = len(list(self.task_repo.list_by_project(project_id)))
        if task_count == self.settings.MAX_TASKS:
            raise ValueError("You have reached maximum number of tasks per project.")
        
        task = Task(
            id = self.task_repo.next_available_id(),
            project_id = project_id,
            name = name,
            description = description,
            status = status,
            deadline = deadline
        )
        task.validate()
        return self.task_repo.add(task)
    
    def delete_task(self, task_id: int) -> bool:
        return self.task_repo.remove(task_id)
    
    def list_tasks_by_project(self, project_id: int) -> Iterable[Task]:
        if self.project_repo.get_by_id(project_id) is None:
            raise ValueError("Project not found.")
        tasks: list = list(self.task_repo.list_by_project(project_id))
        return tasks
    
@dataclass
class UpdateTask:
    """This class handles update procedure for different features of tasks"""
        
    task_repo: TaskRepository
        
    def edit_task_name(self, task_id: int, *, name: str) -> Task:
        task: Task = self.task_repo.get_by_id(task_id)
        if task is None:
           raise ValueError("No Task found.")    
        if not name or len(name.strip()) == 0:
            raise ValueError("Task name cannot be empty")   
        if len(name) > Settings.MAX_NAME_LEN:
            raise ValueError(f"Length of task name cannot be more than {Settings.MAX_NAME_LEN} characters.")
        task.name = name
        return self.task_repo.update(task)
        
    def edit_task_description(self, task_id: int, *, description: str) -> Task:
        task: Task = self.task_repo.get_by_id(task_id)
        if task is None:
            raise ValueError("No Task found.")    
        if len(description) > Settings.MAX_DESCRIPTION_LEN:
            raise ValueError(f"Length of task description cannot be more than {Settings.MAX_DESCRIPTION_LEN} characters.")
        task.description = description            
        return self.task_repo.update(task)
        
    def edit_task_deadline(self, task_id: int, *, deadline: date) -> Task:
        task: Task = self.task_repo.get_by_id(task_id)
        if task is None:
            raise ValueError("No Task found.")    
        task.deadline = deadline           
        return self.task_repo.update(task)
        
    def change_status(self, task_id: int, status: TaskStatus) -> Task:
        task: Task = self.task_repo.get_by_id(task_id)
        if task is None:
            raise ValueError("No Task found.")            
        task.status = status
        return self.task_repo.update(task)
        