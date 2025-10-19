"""Settings loader for the ToDoList application.

Uses python-dotenv to load environment variables. Provides defaults and
validates core numeric limits used by repositories and services.
"""
from __future__ import annotations

from dataclasses import dataclass
import os
from typing import Optional

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    """Immutable settings loaded from environment.

    Attributes:
        MAX_PROJECTS: upper bound for allowed projects in memory
        MAX_TASKS: upper bound for allowed tasks per project in memory
        
        MAX_NAME_LEN: upper bound for length of name of each task or project
        MAX_DESCRIPTION_LEN: upper bound for length of description of each task or project
    """

    MAX_PROJECTS: int = 5
    MAX_TASKS: int = 10
    
    MAX_NAME_LEN: int = 30
    MAX_DESCRIPTION_LEN: int = 150
    

    @staticmethod
    def _parse_int(value: Optional[str], fallback: int) -> int:
        try:
            return int(value) if value is not None else fallback
        except (TypeError, ValueError):
            return fallback

    @classmethod
    def load(cls) -> "Settings":
        """Load settings from environment and .env file.

        Precedence: .env -> OS environment -> defaults.
        """
        load_dotenv()
        MAX_PROJECTS = cls._parse_int(os.getenv("MAX_NUMBER_OF_PROJECT"), fallback = 5)
        MAX_TASKS = cls._parse_int(os.getenv("MAX_NUMBER_OF_TASK"), fallback = 10)
        MAX_NAME_LEN = cls._parse_int(os.getenv("MAX_NAME_LENGTH"), fallback = 30)
        MAX_DESCRIPTION_LEN = cls._parse_int(os.getenv("MAX_DESCRIPTION_LENGTH"), fallback = 150)
        
        MAX_PROJECTS = max(1, MAX_PROJECTS)
        MAX_TASKS = max(1, MAX_TASKS)
        MAX_NAME_LEN = max(1, MAX_NAME_LEN)
        MAX_DESCRIPTION_LEN = max(1, MAX_DESCRIPTION_LEN)
        return cls(MAX_PROJECTS = MAX_PROJECTS, MAX_TASKS = MAX_TASKS, MAX_NAME_LEN = MAX_NAME_LEN, MAX_DESCRIPTION_LEN = MAX_DESCRIPTION_LEN)


