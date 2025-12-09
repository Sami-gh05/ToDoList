from sqlalchemy import Column, Integer, String, Date, Enum, ForeignKey
from sqlalchemy.orm import relationship

from todolist.data.db.sql_db_base import Base

from todolist.config.settings import Settings
from todolist.core.domain.status import TaskStatus

class TaskModel(Base):
    """SQLAlchemy model for Project entity"""
    __tablename__ = "tasks"
    
    settings = Settings.load()

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    name = Column(String(settings.MAX_NAME_LEN), nullable=False)
    description = Column(String(settings.MAX_DESCRIPTION_LEN), nullable=True)
    status = Column(Enum(TaskStatus), nullable=False, default=TaskStatus.TODO)
    deadline = Column(Date, nullable=True)

    project = relationship("ProjectModel", back_populates="tasks")

    def __repr__(self):
        return f"Task(id={self.id}, project_id={self.project_id}, name={self.name}, description={self.description}, status={self.status}, deadline={self.deadline})"

    def __str__(self):
        return f"Task(id={self.id}, project_id={self.project_id}, name={self.name}, description={self.description}, status={self.status}, deadline={self.deadline})"

    def __eq__(self, other):
        return self.id == other.id

        