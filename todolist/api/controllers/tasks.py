from __future__ import annotations

from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Response, status

from todolist.api.controller_schemas.task_request_schema import TaskCreateRequest, TaskUpdateRequest
from todolist.api.controller_schemas.task_response_schema import TaskListResponse, TaskResponse
from todolist.api.dependencies import get_task_service
from todolist.core.domain.status import TaskStatus
from todolist.core.services.task_service import TaskService

router = APIRouter()


@router.get("/", response_model=TaskListResponse, summary="List tasks with filtering and pagination")
def list_tasks(
    skip: int = 0,
    limit: int = 20,
    status: Optional[TaskStatus] = None,
    search: Optional[str] = None,
    due_from: Optional[date] = None,
    due_to: Optional[date] = None,
    sort: Optional[str] = None,
    task_service: TaskService = Depends(get_task_service),
) -> TaskListResponse:
    tasks, total = task_service.list_tasks(
        skip=skip, limit=limit, status=status, search=search, due_from=due_from, due_to=due_to, sort=sort
    )
    return TaskListResponse(items=tasks, total=total, skip=skip, limit=limit)

@router.get("/project/{project_identifier}", response_model=TaskListResponse, summary="List tasks for a project")
def list_tasks_by_project(
    project_identifier: str,
    task_service: TaskService = Depends(get_task_service),
) -> TaskListResponse:
    try:
        tasks = list(task_service.list_tasks_by_project(project_identifier))
    except ValueError as exc:
        message = str(exc)
        code = status.HTTP_404_NOT_FOUND if "not found" in message.lower() else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=code, detail=message) from exc

    total = len(tasks)
    return TaskListResponse(items=tasks, total=total, skip=0, limit=total)



@router.get("/{task_id}", response_model=TaskResponse, summary="Get a task by id")
def get_task(task_id: int, task_service: TaskService = Depends(get_task_service)) -> TaskResponse:
    task = task_service.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED, summary="Create a new task")
def create_task(
    payload: TaskCreateRequest, response: Response, task_service: TaskService = Depends(get_task_service)
) -> TaskResponse:
    try:
        task = task_service.add_task(
            project_identifier=payload.project_id,
            name=payload.name,
            description=payload.description or "",
            status=payload.status,
            deadline=payload.deadline,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    response.headers["Location"] = f"/tasks/{task.id}"
    return task


@router.put("/{task_id}", response_model=TaskResponse, summary="Replace a task")
def replace_task(
    task_id: int, payload: TaskCreateRequest, task_service: TaskService = Depends(get_task_service)
) -> TaskResponse:
    try:
        task = task_service.replace_task(
            task_id,
            name=payload.name,
            description=payload.description,
            status=payload.status,
            deadline=payload.deadline,
            project_id=payload.project_id,
        )
    except ValueError as exc:
        message = str(exc)
        code = status.HTTP_404_NOT_FOUND if "not found" in message.lower() else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=code, detail=message) from exc
    return task


@router.patch("/{task_id}", response_model=TaskResponse, summary="Partially update a task")
def patch_task(
    task_id: int, payload: TaskUpdateRequest, task_service: TaskService = Depends(get_task_service)
) -> TaskResponse:
    try:
        task = task_service.update_task_fields(
            task_id,
            name=payload.name,
            description=payload.description,
            status=payload.status,
            deadline=payload.deadline,
            project_id=payload.project_id,
        )
    except ValueError as exc:
        message = str(exc)
        code = status.HTTP_404_NOT_FOUND if "not found" in message.lower() else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=code, detail=message) from exc
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a task")
def delete_task(task_id: int, task_service: TaskService = Depends(get_task_service)) -> None:
    deleted = task_service.delete_task(task_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return None


@router.patch("/{task_id}/toggle-complete", response_model=TaskResponse, summary="Toggle completion status")
def toggle_task(task_id: int, task_service: TaskService = Depends(get_task_service)) -> TaskResponse:
    try:
        return task_service.toggle_completion(task_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

