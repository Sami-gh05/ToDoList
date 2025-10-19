# ToDoList CLI (Phase 1 – In-Memory Storage)

Python project with layered modules and in-memory repositories.

## Structure
- `todolist/config`: settings loader
- `todolist/core`: domain models, repository interfaces, services
- `todolist/data`: in-memory repository implementations
- `todolist/cli`: simple CLI
- `tests`: placeholder

## Requirements
- Python 3.10–3.12
- Poetry

## Setup
```bash
poetry install
cp .env.example .env
```

## Run
```bash
poetry run todolist
```

## Environment
- `MAX_NUMBER_OF_PROJECT` (default 5)
- `MAX_NUMBER_OF_TASK` (default 10)

## Notes
Phase 1 stores data in memory only. Future phases will add persistence and FastAPI. 
