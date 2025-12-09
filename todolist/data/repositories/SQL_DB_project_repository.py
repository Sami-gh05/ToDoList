from __future__ import annotations

from typing import List

from todolist.core.domain.project import Project
from todolist.core.repositories.project_repository import ProjectRepository
from todolist.data.db.project_model import ProjectModel

from sqlalchemy.orm import Session


class SQL_DB_ProjectRepository(ProjectRepository):
    """SQL Database implementation of project repository"""
    def __init__(self, session: Session) -> None:
        self._session =  session

    @staticmethod
    def _to_domain(orm_model: ProjectModel) -> Project:
        """Convert ORM model to domain model."""
        return Project(id=orm_model.id, name=orm_model.name, description=orm_model.description or "")
    
    @staticmethod
    def _from_domain(domain: Project) -> ProjectModel:
        """Convert domain modelk into ORM model"""
        return ProjectModel (id=domain.id, name=domain.name, description=domain.description or None)


    def add(self, project: Project) -> Project:
        orm_model = ProjectModel (
            name=project.name,
            description=project.description or None
        )
        self._session.add(orm_model)
        self._session.commit()
        return self._to_domain(orm_model)
    
    def get_by_id(self, project_id: int) -> Project | None:
        """Retrieve project by ID."""
        orm_model = self._session.query(ProjectModel).filter(ProjectModel.id == project_id).first()
        return self._to_domain(orm_model) if orm_model else None   
    
    def get_by_name(self, project_name: str) -> Project | None:
        """Retrieve project by name."""
        orm_model = self._session.query(ProjectModel).filter(ProjectModel.name == project_name).first()
        return self._to_domain(orm_model) if orm_model else None
    
    def list_all_projects(self) -> List[Project]:
        """List all projects"""
        orm_models = self._session.query(ProjectModel).all()
        return [self._to_domain(orm_model) for orm_model in orm_models]
    
    def remove(self, project_id: int) -> bool:
        """Remove project by ID."""
        orm_model = self._session.query(ProjectModel).filter(ProjectModel.id == project_id).first()
        if orm_model:
            self._session.delete(orm_model)
            self._session.commit()
            return True
        return False
    
    def update(self, project: Project) -> Project:
        """Update existing project."""
        orm_model = self._session.query(ProjectModel).filter(ProjectModel.id == project.id).first()
        if not orm_model:
            raise ValueError(f"Project with ID {project.id} does not exist.")
        
        orm_model.name = project.name
        orm_model.description = project.description or None
        
        self._session.commit()
        return self._to_domain(orm_model)
