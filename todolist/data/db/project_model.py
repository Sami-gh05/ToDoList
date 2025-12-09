from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from todolist.data.db.session import Base

from todolist.config.settings import Settings

class ProjectModel(Base):
    """SQLAlchemy model for Project entity"""
    __tablename__ = "projects"
    
    settings = Settings.load()
    id = Column(Integer, primary_key=True)
    name = Column(String(settings.MAX_NAME_LEN), nullable=False)
    description = Column(String(settings.MAX_DESCRIPTION_LEN), nullable=True)

    tasks = relationship("TaskModel", back_populates="project", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Project(id={self.id}, name={self.name}, description={self.description})"

    def __str__(self):
        return f"Project(id={self.id}, name={self.name}, description={self.description})"

    def __eq__(self, other):
        return self.id == other.id
        