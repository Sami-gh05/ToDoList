from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional, Iterable

from todolist.core.domain.project import Project

class ProjectRepository(ABC):
    """Abstract repository for projects"""
    
    @abstractmethod
    def next_available_id(self) -> int:
        raise NotImplementedError
    
    @abstractmethod
    def add(self, project: Project) -> Project:
        raise NotImplementedError
    
    @abstractmethod
    def remove(self, project_id: int) -> bool:
        raise NotImplementedError
    
    @abstractmethod
    def get_by_id(self, project_id: int) -> Optional[Project]:
        raise NotImplementedError
    
    @abstractmethod
    def get_by_name(self, project_name: str) -> Optional[Project]:
        raise NotImplementedError
    
    @abstractmethod
    def list_all_projects(self) -> Iterable[Project]:
        raise NotImplementedError
    
    @abstractmethod
    def update(self, project: Project) -> Project:
        raise NotImplementedError