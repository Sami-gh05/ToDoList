from __future__ import annotations

from enum import Enum

class TaskStatus(str, Enum):
    """Enumeration for task statuses"""
    
    TODO = "todo"
    DOING = "doing"
    DONE = "done"
    
    @classmethod
    def from_string(cls, value: str) -> TaskStatus:
        normalized: str = (value or "").strip().lower()
        for status in cls:
            if status.value == normalized:
                return status
        raise ValueError(f"Invalid status: {value!r}. Allowd: {[s.value for s in cls]}")