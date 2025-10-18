from __future__ import annotations

from collections import defaultdict
from typing import DefaultDict, Dict, List, Iterable, Optional, Union

from todolist.core.domain.task import Task
from todolist.core.domain.project import Project
from todolist.core.repositories.task_repository import TaskRepository

class InMemoryTaskRepository(TaskRepository):
    
    def __init__(self) -> None:
        self._tasks: Dict[int, Task] = {}
        # for seaching by project's id
        self._by_project_id: DefaultDict[int, List[int]] = defaultdict(List)
        # for searching by project's name
        self._by_project_name: DefaultDict[str, List[int]] = defaultdict(List)
        self._next_available_id: int = 1
        
    def next_available_id(self) -> int:
        new_id: int = self._next_available_id
        self._next_available_id += 1
        return new_id
    
    def add(self, task: Task) -> Task:
        self._tasks[task.id] = task
        if task.id not in self._by_project_id[task.project_ref.id]:
            self._by_project_id[task.project_ref.id].append(task.id)
        if task.id not in self._by_project_name[task.project_ref.name]:
            self._by_project_name[task.project_ref.name].append(task.id)
        return task
    
    def remove(self, task_id: int) -> bool:
        task = self._tasks.pop(task_id, None)
        if Task is None:
            return False
        if task_id in self._by_project_id.get(task.project_ref.id, []):
            self._by_project_id[task.project_ref.id] = [i for i in self._by_project_id[task.project_ref.id] if i != task_id]
        if task_id in self._by_project_name.get(task.project_ref.name, []):
            self._by_project_name[task.project_ref.name] = [i for i in self._by_project_name[task.project_ref.name] if i != task_id]
        return True
    
    def get_by_id(self, task_id: int) -> Optional[Task]:
        return self._tasks.get(task_id, None)
    
    def list_by_project(self, project_identifier: Union[int, str]) -> Iterable[Task]:
        ids: list
        if isinstance(project_identifier, int):
            # indicates that we wanna find project by id
            ids = self._by_project_id.get(project_identifier, [])
        elif isinstance(project_identifier, str):
            # indicates that we wanna find project by name
            ids = self._by_project_name.get(project_identifier, [])
        return [self._tasks[i] for i in ids]
    
    def remove_by_project(self, project_identifier: Union[int, str]) -> int:
        ids: list
        project: Project
        
        if isinstance(project_identifier, int):
            # indicates that we wanna find project by id
            ids = self._by_project_id.get(project_identifier, [])
        elif isinstance(project_identifier, str):
            # indicates that we wanna find project by name
            ids = self._by_project_name.get(project_identifier, [])
        if ids.count > 0:
            project = self._tasks[ids[0]].project_ref
        count: int = 0
        for i in ids:
            self._tasks.pop(i, None)
            count += 1
        self._by_project_id.pop(project.id, None)
        self._by_project_name.pop(project.name, None)
        
        
    def update(self, task: Task) -> Task:
        if task.id not in self._tasks:
            raise ValueError("Task not found.")
        # ensure project index contains id
        if task.id not in self._by_project_id[task.project_ref.id]:
            self._by_project_id[task.project_ref.id].append(task.id)
        if task.id not in self._by_project_name[task.project_ref.name]:
            self._by_project_name[task.project_ref.name].append(task.id)
        self._tasks[task.id] = task
        return task