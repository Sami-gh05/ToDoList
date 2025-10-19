from __future__ import annotations

from collections import defaultdict
from typing import DefaultDict, Dict, List, Iterable, Optional

from todolist.core.domain.task import Task
from todolist.core.repositories.task_repository import TaskRepository

class InMemoryTaskRepository(TaskRepository):
    
    def __init__(self) -> None:
        self._tasks: Dict[int, Task] = {}
        self._by_project_id: DefaultDict[int, List[int]] = defaultdict(list)
        self._next_available_id: int = 1
        
    def next_available_id(self) -> int:
        new_id: int = self._next_available_id
        self._next_available_id += 1
        return new_id
    
    def add(self, task: Task) -> Task:
        self._tasks[task.id] = task
        if task.id not in self._by_project_id[task.project_id]:
            self._by_project_id[task.project_id].append(task.id)
        return task
    
    def remove(self, task_id: int) -> bool:
        task = self._tasks.pop(task_id, None)
        if task is None:
            return False
        
        if task_id in self._by_project_id.get(task.project_id, []):
            self._by_project_id[task.project_id] = [i for i in self._by_project_id[task.project_id] if i != task_id]
        return True
    
    def get_by_id(self, task_id: int) -> Optional[Task]:
        return self._tasks.get(task_id, None)
    
    def list_by_project(self, project_id: int) -> Iterable[Task]:
        ids: list = self._by_project_id.get(project_id, [])
        return [self._tasks[i] for i in ids]
    
    def remove_by_project(self, project_id: int) -> int:
        ids: list = self._by_project_id.get(project_id, [])        
        count: int = 0
        for i in ids:
            self._tasks.pop(i, None)
            count += 1
        self._by_project_id.pop(project_id, None)
        return count        
        
    def update(self, task: Task) -> Task:
        if task.id not in self._tasks:
            raise ValueError("Task not found.")
        # ensure project index contains id
        if task.id not in self._by_project_id[task.project_id]:
            self._by_project_id[task.project_id].append(task.id)
        self._tasks[task.id] = task
        return task