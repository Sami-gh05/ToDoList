"""Top-level package for the ToDoList application.

Layers:
- config: settings loader and environment configuration
- core: domain entities, repository interfaces, and services
- data: in-memory repository implementations (Phase 1)
- cli: command-line interface for demonstration

Dependency direction:
cli -> core.services -> core.repositories (interfaces) -> data.repositories (implementations)
"""

__all__ = ["__version__"]
__version__ = "0.1.0"


