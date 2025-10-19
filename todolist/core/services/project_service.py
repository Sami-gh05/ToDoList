from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional, Union

from todolist.config.settings import Settings
from todolist.core.domain.project import Project
from todolist.core.repositories.project_repository import ProjectRepository
from todolist.core.repositories.task_repository import TaskRepository

def can_cast_to_int(s: Union[str, int]) -> bool:
    try:
        int(s)
        return True
    except (ValueError, TypeError):
        return False

@dataclass
class ProjectService:
    """Service for managing projects and enforcing business rules
    
    Responsibilities:
    - Enforce name/description constraints (lengths)
    - Enforce unique project names
    - Enforce MAX_NUMBER_OF_PROJECT limit
    - Cascade delete tasks when a project is removed
    """
    
    project_repo: ProjectRepository
    task_rep: TaskRepository
    settings: Settings
    
    def create_project(self, name: str, description: str = "") -> Project:
        if can_cast_to_int(name):
            raise ValueError("Project name cannot be just numbers.")
        if self.project_repo.get_by_name(name) is not None:
            raise ValueError("Project name must be unique.")
        existing_count: int = len(list(self.project_repo.list_all_projects()))
        if existing_count == self.settings.MAX_PROJECTS:
            raise ValueError("You have reached maximum number of projects.")
        project = Project(id = self.project_repo.next_available_id(), name = name, description = description)
        return self.project_repo.add(project)
    
    def delete_project(self, project_identifier: Union[int, str]) -> bool:
        project: Project
        if can_cast_to_int(project_identifier):
            project = self.project_repo.get_by_id(int(project_identifier))
        else:
            project = self.project_repo.get_by_name(project_identifier)
        if project is None:
            return False
        # Cascade deleting tasks
        self.task_rep.remove_by_project(project.id)
        return self.project_repo.remove(project.id)
    
    def list_projects(self) -> Iterable[Project]:
        projects: list = list(self.project_repo.list_all_projects())
        return projects
    
@dataclass  
class UpdateProject:
    """This class handles update procedure for different features of projects"""
    
    project_repo: ProjectRepository
    
    def edit_project_name(self, project_identifier: Union[int, str], *, name: str) -> Project:
        project: Project
        if can_cast_to_int(project_identifier):
            project = self.project_repo.get_by_id(int(project_identifier))
        else:
            project = self.project_repo.get_by_name(project_identifier)
        if project is None:
            raise ValueError("Project not found.")
        if not name or len(name.strip()) == 0:
            raise ValueError("Name of project cannot be empty")
        if name != project.name:
            if self.project_repo.get_by_name(name) is not None:
                raise ValueError("Project name must be unique.")
        if len(name) > Settings.MAX_NAME_LEN:
            raise ValueError(f"Length of project name cannot be more than {Settings.MAX_NAME_LEN} characters.")
        project.name = name
        return self.project_repo.update(project)
    
    def edit_project_description(self, project_identifier: Union[int, str],  *, description: str) -> Project:
        project: Project
        if can_cast_to_int(project_identifier):
            project = self.project_repo.get_by_id(int(project_identifier))
        else:
            project = self.project_repo.get_by_name(project_identifier)
        if project is None:
            raise ValueError("Project not found.")
        if len(description) > Settings.MAX_DESCRIPTION_LEN:
            raise ValueError(f"Length of project description cannot be more than {Settings.MAX_DESCRIPTION_LEN} characters.")
        project.description = description
        return self.project_repo.update(project)
    
    