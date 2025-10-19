from __future__ import annotations

from datetime import datetime
from typing import Callable

from todolist.core.domain.status import TaskStatus
from todolist.core.services.project_service import ProjectService, UpdateProject
from todolist.core.services.task_service import TaskService, UpdateTask


project_service: ProjectService
task_service: TaskService
project_update: UpdateProject
task_update: UpdateTask

def run_menu(project_service: ProjectService, task_service: TaskService) -> None:
    actions = {
        "1": ("Create project", lambda: _create_project(project_service)),
        "2": ("Edit project", lambda: _run_edit_project_menu(project_update)),
        "3": ("Delete project", lambda: _delete_project(project_service)),
        "4": ("List projects", lambda: _list_projects(project_service)),
        "5": ("Add task", lambda: _add_task(task_service)),
        "6": ("Edit task", lambda: _run_edit_task_menu(task_update)),
        "7": ("Delete task", lambda: _delete_task(task_service)),
        "8": ("List tasks by project", lambda: _list_tasks(task_service)),
        "0": ("Exit", None),
    }

    while True:
        print("\nChoose an action:")
        for key, (label, _) in actions.items():
            print(f"  {key}. {label}")
        choice = input("> ").strip()
        if choice == "0":
            print("Goodbye!")
            break
        action = actions.get(choice)
        if not action:
            print("Invalid choice.")
            continue
        try:
            handler = action[1]
            if handler:
                handler()
        except Exception as exc:
            print(f"Error: {exc}")


def _run_edit_project_menu(project_update: UpdateProject) -> None:
    print("Edit project:")
    project_edit_actions = {
        "1": ("Edit name", lambda: _edit_project_name(project_update)),
        "2": ("Edit description", lambda: _edit_project_description(project_update)),
        "0": ("Back", lambda: run_menu(project_service, task_service))
    }
    
    while(True):
        for key, (label, _) in project_edit_actions.items():
            print(f"  {key}. {label}")
        choice = input("> ").strip()
        if choice == "0":
            run_menu(project_service, task_service)

        action = project_edit_actions.get(choice)
        if not action:
            print("Invalid choice.")
            continue
        try:
            handler = project_edit_actions[1]
            if handler:
                handler()
        except Exception as exc:
            print(f"Error: {exc}")
  
    
def _edit_project_name(project_update: UpdateProject) -> None:
    pid = int(input("Project id: "))
    name = input("New name: ") or None
    proj = project_update.edit_project_name(pid, name=name)
    print(f"Updated project #{proj.id}.")
  
    
def _edit_project_description(project_update: UpdateProject) -> None:
    pid = int(input("Project id: "))
    description = input("New description: ") or None
    proj = project_update.edit_project_description(pid, description = description)
    print(f"Updated project #{proj.id}.")
    
    
def _create_project(project_service: ProjectService) -> None:
    name = input("Project name: ")
    description = input("Project description: ")
    project = project_service.create_project(name, description)
    print(f"Created project #{project.id}.")


def _delete_project(project_service: ProjectService) -> None:
    pid = int(input("Project id: "))
    ok = project_service.delete_project(pid)
    print("Deleted." if ok else "Project not found.")


def _list_projects(project_service: ProjectService) -> None:
    projects = list(project_service.list_projects())
    if not projects:
        print("No projects found.")
        return
    print("Projects:")
    for p in projects:
        print(f"- #{p.id} {p.name}: {p.description}")  
  
        
def _run_edit_task_menu(task_update: UpdateTask) -> None:
    print("Edit task:")
    task_edit_actions = {
        "1": ("Edit name", lambda: _edit_task_name(task_update)),
        "2": ("Edit description", lambda: _edit_task_description(task_update)),
        "3": ("Edit status[todo|doing|done]:", lambda: _change_task_status(task_update)),
        "4": ("Edit deadline (YYYY-MM-DD):", lambda: _edit_task_deadline(task_update)),
        "0": ("Back", lambda: run_menu(project_service, task_service))
    }
    
    while(True):
        for key, (label, _) in task_edit_actions.items():
            print(f"  {key}. {label}")
        choice = input("> ").strip()
        if choice == "0":
            run_menu(project_service, task_service)

        action = task_edit_actions.get(choice)
        if not action:
            print("Invalid choice.")
            continue
        try:
            handler = task_edit_actions[1]
            if handler:
                handler()
        except Exception as exc:
            print(f"Error: {exc}")


def _edit_task_name(task_update: UpdateTask) -> None:
    tid = int(input("Task id: "))
    name = input("New name: ") or None
    task = task_update.edit_task_name(tid, name = name)
    print(f"Updated task #{task.id}.")
    

def _edit_task_description(task_update: UpdateTask) -> None:
    tid = int(input("Task id: "))
    description = input("New description: ") or None
    task = task_update.edit_task_description(tid, description = description)
    print(f"Updated task #{task.id}.")
    
    
def _change_task_status(task_update: UpdateTask) -> None:
    tid = int(input("Task id: "))
    status_in = input("New status [todo|doing|done]: ").strip()
    status = TaskStatus.from_string(status_in) if status_in else None
    task = task_update.change_status(tid, status = status)
    print(f"Updated task #{task.id}.")
    
    
def _edit_task_deadline(task_update: UpdateTask) -> None:
    tid = int(input("Task id: "))
    deadline_str = input("New deadline YYYY-MM-DD: ").strip()
    deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date() if deadline_str else None
    task = task_update.edit_task_deadline(tid, deadline = deadline)
    print(f"Updated task #{task.id}.")


def _add_task(task_service: TaskService) -> None:
    pid = int(input("Project id: "))
    title = input("Task title: ")
    description = input("Task description: ")
    status_str = input("Status [todo|doing|done] (default todo): ").strip() or "todo"
    deadline_str = input("Deadline (YYYY-MM-DD, optional): ").strip()
    deadline = None
    if deadline_str:
        deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date()
    task = task_service.add_task(
        pid,
        title=title,
        description=description,
        status=TaskStatus.from_string(status_str),
        deadline=deadline,
    )
    print(f"Created task #{task.id}.")


def _delete_task(task_service: TaskService) -> None:
    tid = int(input("Task id: "))
    ok = task_service.delete_task(tid)
    print("Deleted." if ok else "Task not found.")


def _list_tasks(task_service: TaskService) -> None:
    pid = int(input("Project id: "))
    try:
        tasks = list(task_service.list_tasks_by_project(pid))
    except Exception as exc:  # noqa: BLE001
        print(f"Error: {exc}")
        return
    if not tasks:
        print("No tasks found.")
        return
    print("Tasks:")
    for t in tasks:
        deadline = t.deadline.isoformat() if t.deadline else "-"
        print(f"- #{t.id} {t.title} [{t.status.value}] due {deadline}")


