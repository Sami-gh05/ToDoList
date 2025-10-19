from __future__ import annotations

from typing import Dict, Iterable, Optional

from todolist.core.domain.project import Project
from todolist.core.repositories.project_repository import ProjectRepository

class InMemoryProjectRepository(ProjectRepository):
    """In-memory implementaion of project repository"""
    
    def __init__(self) -> None:
        self._projects: Dict[int, Project] = {}
        self._name_index: Dict[str, int] = {}
        self._next_available_id: int = 1
        
    def next_available_id(self) -> int:
        new_id = self._next_available_id
        self._next_available_id += 1
        return new_id
    
    def add(self, project: Project) -> Project:
        self._projects[project.id] = project
        self._name_index[project.name.lower()] = project.id
        return project
    
    def remove(self, project_id: int) -> bool:
        project = self._projects.pop(project_id, None)
        if project is None:
            return False
        # remove name index
        lowered_name = project.name.lower()
        if self._name_index.get(lowered_name) == project_id:
            self._name_index.pop(lowered_name, None)
        return True
    
    def get_by_id(self, project_id: int) -> Optional[Project]:
        return self._projects.get(project_id)
    
    def get_by_name(self, project_name: str) -> Optional[Project]:
        project_id: int = self._name_index.get(project_name.lower())
        return self._projects.get(project_id, None)
    
    def list_all_projects(self) -> Iterable[Project]:
        return list(self._projects.values())
    
    def update(self, project: Project) -> Project:
        if project.id not in self._projects:
            raise ValueError("Project not found.")
        self._projects[project.id] = project
        self._name_index[project.name.lower()] = project.id
        return project