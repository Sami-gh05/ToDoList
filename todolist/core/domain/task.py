from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, date
from typing import Optional

from todolist.core.domain.status import TaskStatus
from todolist.config.settings import Settings

@dataclass
class Task:
    """Task entity belonging to a project by project_id
    
    This class only contains the meta info and business logic, and otehr 
    parts are handled in repository and service layer."""
    
    id: int
    name: str
    description: str = ""
    status: TaskStatus = field(default = TaskStatus.TODO)
    deadline: Optional[date] = None
    
    def __post_init__(self):
        # validate the Task object right after being created
        self.validate()
    
    def validate(self) -> None:
        if not self.name or len(self.name.strip()) == 0:
            raise ValueError("Task name cannot be empty.")
        if len(self.name.strip()) > Settings.MAX_NAME_LEN:
            raise ValueError(f"Task name should be less than {Settings.MAX_NAME_LEN} characters.")
        if len(self.description.strip()) > Settings.MAX_DESCRIPTION_LEN:
            raise ValueError(f"Task description should be less than {Settings.MAX_DESCRIPTION_LEN} characters.")
        
        