# ToDoList Application - CLI + FastAPI (PostgreSQL Backend)

A task management application with both a command-line menu and a FastAPI REST API, built with Python and PostgreSQL. The project demonstrates software engineering principles including domain-driven design, repository pattern, separation of concerns, and database migrations.

## 🚀 Features

### Project Management
- **Create Projects**: Add new projects with names and descriptions
- **Edit Projects**: Modify project names and descriptions
- **Delete Projects**: Remove projects (automatically deletes associated tasks via cascade)
- **List Projects**: View all available projects persisted in PostgreSQL

### Task Management
- **Add Tasks**: Create tasks within projects with names, descriptions, status, and deadlines
- **Edit Tasks**: Modify task names, descriptions, status, and deadlines
- **Delete Tasks**: Remove individual tasks
- **List Tasks**: View all tasks within a specific project

### Task Status Management
- **Status Types**: TODO, DOING, DONE
- **Status Updates**: Change task status through the edit interface
- **Deadline Support**: Set and modify task deadlines (YYYY-MM-DD format)
- **Automatic Closure**: Scheduler automatically closes overdue incomplete tasks and sets `closed_at` timestamp

### Flexible Project Identification
- **ID or Name**: Use either project ID (number) or project name (string) for all operations
- **Case-Insensitive Search**: Project names are matched case-insensitively

### Background Scheduler
- **Overdue Task Detection**: Automatically detects tasks past their deadline that are not completed
- **Auto-Close Tasks**: Marks overdue tasks as DONE and records closure timestamp
- **Configurable Intervals**: Runs on a scheduled basis without blocking CLI

## 🏗️ Architecture

The application follows a clean architecture pattern with clear separation of concerns:

```
todolist/
├── alembic/                    # Database migrations
│   ├── versions/              # Migration scripts
│   ├── env.py                 # Migration environment config
│   └── script.py.mako         # Migration template
├── cli/                        # Command-line interface layer
│   └── menu.py                # Interactive menu system
├── config/                     # Configuration management
│   └── settings.py            # Environment-based settings
├── core/                       # Business logic layer
│   ├── domain/                # Domain entities
│   │   ├── project.py         # Project entity
│   │   ├── task.py            # Task entity
│   │   └── status.py          # Task status enumeration
│   ├── repositories/          # Repository interfaces
│   │   ├── project_repository.py
│   │   └── task_repository.py
│   └── services/              # Business services
│       ├── project_service.py
│       ├── task_service.py
│       └── scheduler_service.py  # Background scheduler
├── data/                       # Data access layer
│   ├── db/                    # Database configuration
│   │   ├── project_model.py   # SQLAlchemy Project model
│   │   ├── task_model.py      # SQLAlchemy Task model
│   │   ├── session.py         # Database session factory
│   │   └── sql_db_base.py     # SQLAlchemy declarative base
│   └── repositories/          # Repository implementations
│       ├── SQL_DB_project_repository.py
│       └── SQL_DB_task_repository.py
├── main.py                     # Application entry point
├── alembic.ini                # Alembic configuration
└── .env                       # Environment variables (not in git)
```

### Design Patterns

- **Repository Pattern**: Abstracts data access with interfaces and SQL implementations
- **Service Layer**: Encapsulates business logic and validation
- **Domain-Driven Design**: Clear separation between domain entities and infrastructure
- **Dependency Injection**: Services receive dependencies through constructor injection
- **ORM Mapping**: SQLAlchemy for database abstraction and type-safe queries
- **Migration Management**: Alembic for versioned database schema changes

## 📋 Requirements

- Python 3.8+
- PostgreSQL 12+
- Docker (optional, for PostgreSQL container)
- Poetry (recommended for dependency management)

### Dependencies
- python-dotenv (environment configuration)
- sqlalchemy (ORM)
- psycopg2 (PostgreSQL driver)
- alembic (database migrations)
- schedule (background task scheduling)

## 🛠️ Installation & Setup

### Option 1: Using Poetry with Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd todolist
   ```

2. **Start PostgreSQL with Docker**
   ```bash
   docker run --name postgresql -e POSTGRES_USER=<user> -e POSTGRES_PASSWORD=<pass> -e POSTGRES_DB=<db> -p 5432:5432 -d postgres:latest
   ```

3. **Create `.env` file in project root**
   See .env.example file.

4. **Install dependencies**
   ```bash
   poetry install
   ```

5. **Run the application** (migrations apply automatically on startup)
   - CLI (interactive menu):
     ```bash
     poetry run python -m todolist.main
     ```
   - API (FastAPI + Uvicorn):
     ```bash
     poetry run uvicorn todolist.api.main:app --reload --host 0.0.0.0 --port 8000
     ```

### Database Migrations

Migrations are applied automatically when the app starts. To manually manage migrations:

```bash
# Create a new migration after model changes
alembic revision --autogenerate -m "Description of changes"

# Apply all pending migrations
alembic upgrade head

# View migration history
alembic history

# Rollback to previous migration
alembic downgrade -1
```

## 🎮 Usage

### Option A: CLI (Phase 2 experience)
Run:
```bash
poetry run python -m todolist.main
```

The CLI will:
1. Apply any pending database migrations
2. Start the background scheduler
3. Display the interactive menu

Main Menu Options
```
ToDoList CLI (Phase 2 - PostgreSQL Backend)

Choose an action:
  1. Create project
  2. Edit project
  3. Delete project
  4. List projects
  5. Add task
  6. Edit task
  7. Delete task
  8. List tasks by project
  0. Exit
```

Example Workflow

1. **Create a Project**
   - Select option 1
   - Enter project name: "Web Development"
   - Enter description: "Personal website project"

2. **Add Tasks**
   - Select option 5
   - Enter project ID or name: "Web Development"
   - Enter task name: "Design homepage"
   - Enter description: "Create wireframes and mockups"
   - Enter status: "todo" (or press Enter for default)
   - Enter deadline: "2024-02-15" (optional)

3. **List Tasks**
   - Select option 8
   - Enter project ID or name: "Web Development"
   - View all tasks with their status and deadlines

4. **Edit Tasks**
   - Select option 6
   - Choose what to edit (name, description, status, deadline)
   - Enter task ID and new values

5. **Automatic Task Closure**
   - Scheduler runs periodically in background
   - Incomplete tasks with past deadlines are automatically marked DONE
   - `closed_at` timestamp is recorded

### Option B: REST API (FastAPI - Phase 3)
Run:
```bash
poetry run uvicorn todolist.api.main:app --reload --host 0.0.0.0 --port 8000
```

Explore:
- Docs (Swagger): `http://localhost:8000/docs`
- Docs (ReDoc): `http://localhost:8000/redoc`
- Health check: `http://localhost:8000/health`

Quick examples (replace values as needed):
- Create project
  ```bash
  curl -X POST http://localhost:8000/projects/ \
    -H "Content-Type: application/json" \
    -d '{"name":"Web Dev","description":"Personal site"}'
  ```
- List projects
  ```bash
  curl http://localhost:8000/projects/
  ```
- Create task (project can be id or name)
  ```bash
  curl -X POST http://localhost:8000/tasks/ \
    -H "Content-Type: application/json" \
    -d '{"project_id":"Web Dev","name":"Design homepage","description":"Wireframes","status":"TODO","deadline":"2025-02-15"}'
  ```
- Update task
  ```bash
  curl -X PATCH http://localhost:8000/tasks/1 \
    -H "Content-Type: application/json" \
    -d '{"status":"DONE","description":"Finished"}'
  ```
- Delete task
  ```bash
  curl -X DELETE http://localhost:8000/tasks/1
  ```

## ⚙️ Configuration

### Environment Variables
Located in `.env` file (template is like `.env.example`):

- `DB_USER`: PostgreSQL username
- `DB_PASS`: PostgreSQL password
- `DB_HOST`: PostgreSQL host (default: localhost)
- `DB_PORT`: PostgreSQL port (default: 5432)
- `DB_NAME`: Database name
- `MAX_NUMBER_OF_PROJECT`: Maximum projects allowed (default: 10)
- `MAX_NUMBER_OF_TASK`: Maximum tasks per project (default: 20)
- `MAX_NAME_LENGTH`: Maximum length for names (default: 50)
- `MAX_DESCRIPTION_LENGTH`: Maximum length for descriptions (default: 200)

## 🔧 Development

### Project Structure
- **Domain Layer**: Business entities and rules (database-agnostic)
- **Service Layer**: Implements business logic and validation
- **Repository Layer**: Abstracts data access with SQL implementation
- **CLI Layer**: Provides user interface
- **Data Layer**: SQLAlchemy models and database configuration

### Key Components

#### Domain Entities
- **Project**: ID, name, description
- **Task**: ID, project reference, name, description, status, deadline, closed_at timestamp
- **TaskStatus**: Enumeration (TODO, DOING, DONE)

#### Services
- **ProjectService**: Project CRUD operations and business rules
- **TaskService**: Task CRUD operations and status management
- **SchedulerService**: Background job for overdue task closure

#### Data Models (SQLAlchemy)
- **ProjectModel**: Maps to `projects` table
- **TaskModel**: Maps to `tasks` table with foreign key to projects

#### Repositories
- **SQL_DB_ProjectRepository**: PostgreSQL persistence for projects
- **SQL_DB_TaskRepository**: PostgreSQL persistence for tasks

### Database Schema

**Projects Table**
```sql
CREATE TABLE projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL UNIQUE,
    description VARCHAR(200)
);
```

**Tasks Table**
```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL REFERENCES projects(id),
    name VARCHAR(50) NOT NULL,
    description VARCHAR(200),
    status ENUM('TODO', 'DOING', 'DONE') NOT NULL DEFAULT 'TODO',
    deadline DATE,
    closed_at TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);
```

## 📝 License

This project is part of a Software Engineering course and is intended for educational purposes.

## 📊 Version History

- **v0.2.0**: Phase 2 - PostgreSQL Backend
  - PostgreSQL database persistence (replacing in-memory storage)
  - SQLAlchemy ORM for type-safe database access
  - Alembic for database migrations
  - Background scheduler for overdue task management
  - Cascade delete for project-task relationships
  - Automatic schema migration on application startup
  - Connection pooling and session management

- **v0.1.0**: Phase 1 - In-Memory Backend
  - In-memory data storage
  - CLI interface
  - Project and task CRUD operations
  - Task status management
  - Flexible project identification

---

**Note**: Current release is Phase 3: the FastAPI REST API served via Uvicorn, sharing the same PostgreSQL database, migrations, and business logic as the CLI. Phase 2 introduced the PostgreSQL-backed CLI with scheduler; that flow still works alongside the API.