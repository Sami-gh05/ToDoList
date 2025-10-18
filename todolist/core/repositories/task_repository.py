from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable, Optional

from todolist.core.domain.task import Task

class TaskRepository(ABC):
    "Abstract methods for tasks' repository"
    
    @abstractmethod
    def next_available_id(self) -> int:
        raise NotImplementedError
    
    @abstractmethod
    def add(self, task: Task) -> Task:
        raise NotImplementedError
    
    @abstractmethod
    def remove(self, task_id: int) -> bool:
        raise NotImplementedError
    
    @abstractmethod
    def get_by_id(self, task_id: int) -> Optional[Task]:
        raise NotImplementedError
    
    @abstractmethod
    def list_by_project(self, project_id: int) -> Iterable[Task]:
        """List tasks by project name or id"""
        raise NotImplementedError
    
    @abstractmethod
    def remove_by_project(self, project_id: int) -> int:
        """Remove all tasks by project name or id; return count removed"""
        raise NotImplementedError
    
    @abstractmethod
    def update(self, task: Task) -> Task:
        raise NotImplementedError