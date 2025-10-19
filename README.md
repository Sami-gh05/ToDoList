# ToDoList CLI Application

A command-line task management application built with Python, featuring a clean architecture and in-memory data storage. This project demonstrates software engineering principles including domain-driven design, repository pattern, and separation of concerns.

## 🚀 Features

### Project Management
- **Create Projects**: Add new projects with names and descriptions
- **Edit Projects**: Modify project names and descriptions
- **Delete Projects**: Remove projects (automatically deletes associated tasks)
- **List Projects**: View all available projects

### Task Management
- **Add Tasks**: Create tasks within projects with names, descriptions, status, and deadlines
- **Edit Tasks**: Modify task names, descriptions, status, and deadlines
- **Delete Tasks**: Remove individual tasks
- **List Tasks**: View all tasks within a specific project

### Task Status Management
- **Status Types**: TODO, DOING, DONE
- **Status Updates**: Change task status through the edit interface
- **Deadline Support**: Set and modify task deadlines (YYYY-MM-DD format)

### Flexible Project Identification
- **ID or Name**: Use either project ID (number) or project name (string) for all operations
- **Consistent Interface**: Same commands work with both identification methods

## 🏗️ Architecture

The application follows a clean architecture pattern with clear separation of concerns:

```
todolist/
├── cli/                    # Command-line interface layer
│   └── menu.py            # Interactive menu system
├── config/                # Configuration management
│   └── settings.py        # Environment-based settings
├── core/                  # Business logic layer
│   ├── domain/           # Domain entities
│   │   ├── project.py    # Project entity
│   │   ├── task.py       # Task entity
│   │   └── status.py     # Task status enumeration
│   ├── repositories/     # Repository interfaces
│   │   ├── project_repository.py
│   │   └── task_repository.py
│   └── services/         # Business services
│       ├── project_service.py
│       └── task_service.py
├── data/                 # Data access layer
│   └── repositories/     # Repository implementations
│       ├── in_memory_project_repository.py
│       └── in_memory_task_repository.py
└── main.py              # Application entry point
```

### Design Patterns

- **Repository Pattern**: Abstracts data access with interfaces and implementations
- **Service Layer**: Encapsulates business logic and validation
- **Domain-Driven Design**: Clear separation between domain entities and infrastructure
- **Dependency Injection**: Services receive dependencies through constructor injection

## 📋 Requirements

- Python 3.8+
- python-dotenv (for environment configuration)

## 🛠️ Installation

### Option 1: Using pip

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd todolist
   ```

2. **Install dependencies**
   ```bash
   pip install python-dotenv
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

### Option 2: Using Poetry (Recommended)

1. **Install Poetry** (if not already installed)
   ```bash
   # On Windows (PowerShell)
   (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
   
   # On macOS/Linux
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd todolist
   ```

3. **Install dependencies and create virtual environment**
   ```bash
   poetry install
   ```

4. **Run the application**
   ```bash
   poetry run python main.py
   ```
   or
   ```bash
   poetry run todolist
   ```

   Or activate the virtual environment first:
   ```bash
   poetry shell
   python main.py
   ```

## 🎮 Usage

### Starting the Application
```bash
python main.py
```

### Main Menu Options
```
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

### Example Workflow

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

## ⚙️ Configuration

The application supports environment-based configuration through `.env` files or environment variables:

### Environment Variables
- `MAX_NUMBER_OF_PROJECT`: Maximum projects allowed (default: 5)
- `MAX_NUMBER_OF_TASK`: Maximum tasks per project (default: 10)
- `MAX_NAME_LENGTH`: Maximum length for names (default: 30)
- `MAX_DESCRIPTION_LENGTH`: Maximum length for descriptions (default: 150)

### Example .env File
```env
MAX_NUMBER_OF_PROJECT=10
MAX_NUMBER_OF_TASK=20
MAX_NAME_LENGTH=50
MAX_DESCRIPTION_LENGTH=200
```

## 🔧 Development

### Project Structure
- **Domain Layer**: Contains business entities and rules
- **Service Layer**: Implements business logic and validation
- **Repository Layer**: Abstracts data access
- **CLI Layer**: Provides user interface

### Key Components

#### Domain Entities
- **Project**: Represents a project with ID, name, and description
- **Task**: Represents a task with ID, project reference, name, description, status, and deadline
- **TaskStatus**: Enumeration for task states (TODO, DOING, DONE)

#### Services
- **ProjectService**: Manages project operations and business rules
- **TaskService**: Manages task operations within project context

#### Repositories
- **InMemoryProjectRepository**: In-memory storage for projects
- **InMemoryTaskRepository**: In-memory storage for tasks

### Adding New Features

1. **Domain Changes**: Modify entities in `core/domain/`
2. **Business Logic**: Update services in `core/services/`
3. **Data Access**: Implement repository interfaces in `data/repositories/`
4. **User Interface**: Add CLI options in `cli/menu.py`

## 🧪 Testing

The application includes comprehensive error handling and validation:

- **Input Validation**: All user inputs are validated
- **Business Rules**: Enforced through service layer
- **Error Handling**: Graceful error messages for invalid operations
- **Type Safety**: Full type hints throughout the codebase

## 📝 License

This project is part of a Software Engineering course and is intended for educational purposes.

## 📊 Version History

- **v0.1.0**: Initial release with basic project and task management functionality
  - In-memory data storage
  - CLI interface
  - Project and task CRUD operations
  - Task status management
  - Flexible project identification

---

**Note**: This is Phase 1 of the ToDoList application, featuring in-memory storage. Future phases may include database persistence, web interface, and additional features.
