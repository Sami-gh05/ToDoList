from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional

from todolist.config.settings import Settings

@dataclass
class Project:
    """Project aggregate root containing meta info.
    
    Projects are stored separatedly in repositories; this model carries identity
    and metadata only. Cascade behaviors are handled in teh service layer.
    """
    
    id: int
    name: str
    description: str = ""
    
    def __post_init__(self):
        """Auto-validate after construction"""
        self.validate()
    
    def validate(self) -> None:
        if not self.name or len(self.name.strip()) == 0:
            raise ValueError("Project name cannot be empty.")
        if len(self.name) > Settings.MAX_NAME_LEN:
            raise ValueError(f"Project name must be less than {Settings.MAX_NAME_LEN} characters.")
        if len(self.description) > Settings.MAX_DESCRIPTION_LEN:
            raise ValueError(f"Project description must be less than {Settings.MAX_DESCRIPTION_LEN} characters.")
        