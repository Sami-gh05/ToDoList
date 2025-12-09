from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from todolist.config.settings import Settings


class ProjectCreateRequest(BaseModel):
    name: str = Field(..., max_length=Settings.MAX_NAME_LEN, examples=["Web Development"])
    description: Optional[str] = Field(None, max_length=Settings.MAX_DESCRIPTION_LEN, examples=["Personal website"])


class ProjectUpdateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: Optional[str] = Field(None, max_length=Settings.MAX_NAME_LEN)
    description: Optional[str] = Field(None, max_length=Settings.MAX_DESCRIPTION_LEN)

