from __future__ import annotations

from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from todolist.config.settings import Settings
from todolist.core.domain.status import TaskStatus


class TaskCreateRequest(BaseModel):
    project_id: int = Field(..., examples=[1])
    name: str = Field(..., max_length=Settings.MAX_NAME_LEN, examples=["Design homepage"])
    description: Optional[str] = Field(None, max_length=Settings.MAX_DESCRIPTION_LEN, examples=["Create wireframes"])
    status: TaskStatus = Field(default=TaskStatus.TODO, examples=[TaskStatus.TODO])
    deadline: Optional[date] = Field(None, examples=["2025-12-31"])


class TaskUpdateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: Optional[str] = Field(None, max_length=Settings.MAX_NAME_LEN)
    description: Optional[str] = Field(None, max_length=Settings.MAX_DESCRIPTION_LEN)
    status: Optional[TaskStatus] = None
    deadline: Optional[date] = None
    project_id: Optional[int] = Field(None, examples=[1])

