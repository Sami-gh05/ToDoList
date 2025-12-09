from __future__ import annotations

from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import func

from todolist.core.domain.task import Task
from todolist.core.repositories.task_repository import TaskRepository
from todolist.data.db.task_model import TaskModel

class SQL_DB_TaskRepository(TaskRepository):
    """SQL Database implementation of task repository"""
    def __init__(self, session: Session) -> None:
        self._session = session
        
    @staticmethod
    def _to_domain(orm_model: TaskModel) -> Task:
        """Convert ORM model to domain model."""
        return Task(
            id=orm_model.id,
            project_id=orm_model.project_id,
            name=orm_model.name,
            description=orm_model.description or "",
            status=orm_model.status,
            deadline=orm_model.deadline or None
        )
        
    @staticmethod
    def _from_domain(domain: Task) -> TaskModel:
        """Convert domain model into ORM model."""
        return TaskModel(
            id=domain.id or None,  # SQLAlchemy will set this after insert
            project_id=domain.project_id,
            name=domain.name,
            description=domain.description or None,
            status=domain.status,
            deadline=domain.deadline or None
        )
        
    def add(self, task: Task) -> Task:
        orm_model = TaskModel(
            name = task.name,
            project_id = task.project_id,
            description = task.description or None,
            status = task.status,
            deadline = task.deadline or None
        )
        self._session.add(orm_model)
        self._session.commit()
        return self._to_domain(orm_model)
    
    def get_by_id(self, task_id: int) -> Task | None:
        """Retrieve task by ID."""
        orm_model = self._session.query(TaskModel).filter(TaskModel.id == task_id).first()
        return self._to_domain(orm_model) if orm_model else None
    
    def list_by_project(self, project_id: int) -> List[Task]:
        """List all tasks for a given project."""
        orm_models: List[TaskModel] = self._session.query(TaskModel).filter(TaskModel.project_id == project_id).all()
        return [self._to_domain(orm_model) for orm_model in orm_models]
    
    def remove(self, task_id: int) -> bool:
        """Remove task by ID."""
        orm_model = self._session.query(TaskModel).filter(TaskModel.id == task_id).first()
        if orm_model:
            self._session.delete(orm_model)
            self._session.commit()
            return True
        return False

    def remove_by_project(self, project_id: int) -> int:
        """Remove all tasks for a given project. Return number of deleted tasks"""
        deleted_count = self._session.query(TaskModel).filter(TaskModel.project_id == project_id).delete()
        self._session.commit()
        return deleted_count
    
    def update(self, task: Task) -> Task:
        """Update existing task."""
        orm_model = self._session.query(TaskModel).filter(TaskModel.id == task.id).first()
        if not orm_model:
            raise ValueError(f"Task with ID {task.id} does not exist.")
        
        orm_model.name = task.name
        orm_model.project_id = task.project_id
        orm_model.description = task.description or None
        orm_model.status = task.status
        orm_model.deadline = task.deadline or None
        
        self._session.commit()
        return self._to_domain(orm_model)