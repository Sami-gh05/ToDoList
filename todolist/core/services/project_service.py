from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional, Union

from todolist.config.settings import Settings
from todolist.core.domain.project import Project
from todolist.core.repositories.project_repository import ProjectRepository
from todolist.core.repositories.task_repository import TaskRepository

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
    task_repo = TaskRepository
    settings = Settings
    
    def creat_project(self, name: str, description: str = "") -> Project:
        if self.project_repo.get_by_name(name) is not None:
            raise ValueError("Project name must be unique.")
        
        existing_count: int = len(list(self.project_repo.list_all_projects))
        if existing_count == self.settings.MAX_PROJECTS:
            raise ValueError("You have reached maximum number of projects.")
        
        project = Project(id = self.project_repo.next_available_id(), name = name, description = description)
        
        return self.project_repo.add(project)
    
    def delete_project(self, project_identifier: Union[int, str]) -> bool:
        project: Project
        if isinstance(project_identifier, int):
            project = self.project_repo.get_by_id(project_identifier)
        elif isinstance(project_identifier, str):
            project = self.project_repo.get_by_name(project_identifier)
            
        if project is None:
            return False
        
        # Cascade deleting tasks
        self.task_repo.remove_by_project(project.id)
        return self.project_repo.remove(project.id)
    
    def list_projects(self) -> Iterable[Project]:
        projects: list = list(self.project_repo.list_all_projects())
        return projects
    
@dataclass  
class UpdateProject:
    """This class handles update procedure for different features of projects"""
    
    project_repo: ProjectRepository
    
    def edit_project_name(self, project_id: int, *, name: str) -> Project:
        project: Project = self.project_repo.get_by_id(project_id)
    
        if project is None:
            raise ValueError("Project not found.")
        
        if name != project.name:
            if self.project_repo.get_by_name(name) is not None:
                raise ValueError("Project name must be unique.")
            
        tempProject = Project(project.name, project.description)
        tempProject.name = name
        tempProject.validate()
        return self.project_repo.update(tempProject)
    
    def edit_project_description(self, project_id: int,  *, description: str) -> Project:
        project: Project = self.project_repo.get_by_id(project_id)
        
        if project is None:
            raise ValueError("Project not found.")
        
        tempProject = Project(project.name, project.description)
        tempProject.description = description
        tempProject.validate()
        return self.project_repo.update(tempProject)
    
    