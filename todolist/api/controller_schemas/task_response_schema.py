from __future__ import annotations

from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from todolist.core.domain.status import TaskStatus


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., examples=[1])
    project_id: int = Field(..., examples=[1])
    name: str
    description: Optional[str] = None
    status: TaskStatus
    deadline: Optional[date] = None
    closed_at: Optional[datetime] = None


class TaskListResponse(BaseModel):
    items: List[TaskResponse]
    total: int
    skip: int
    limit: int

