from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from todolist.api.controller_schemas.project_request_schema import ProjectCreateRequest, ProjectUpdateRequest
from todolist.api.controller_schemas.project_response_schema import ProjectResponse
from todolist.api.dependencies import get_project_service
from todolist.core.services.project_service import ProjectService

router = APIRouter()


@router.get("/", response_model=list[ProjectResponse], summary="List projects")
def list_projects(project_service: ProjectService = Depends(get_project_service)) -> list[ProjectResponse]:
    return list(project_service.list_projects())


@router.get("/{project_id}", response_model=ProjectResponse, summary="Get project by id or name")
def get_project(project_id: str, project_service: ProjectService = Depends(get_project_service)) -> ProjectResponse:
    project = project_service.get_project(project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project


@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED, summary="Create project")
def create_project(payload: ProjectCreateRequest, project_service: ProjectService = Depends(get_project_service)) -> ProjectResponse:
    try:
        return project_service.create_project(name=payload.name, description=payload.description or "")
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.put("/{project_id}", response_model=ProjectResponse, summary="Replace project")
def replace_project(
    project_id: str, payload: ProjectCreateRequest, project_service: ProjectService = Depends(get_project_service)
) -> ProjectResponse:
    project = project_service.get_project(project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    try:
        updated = project_service.edit_project_name(project.id, name=payload.name)
        updated = project_service.edit_project_description(updated.id, description=payload.description or "")
        return updated
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.patch("/{project_id}", response_model=ProjectResponse, summary="Partially update project")
def patch_project(
    project_id: str, payload: ProjectUpdateRequest, project_service: ProjectService = Depends(get_project_service)
) -> ProjectResponse:
    project = project_service.get_project(project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    try:
        if payload.name is not None:
            project = project_service.edit_project_name(project.id, name=payload.name)
        if payload.description is not None:
            project = project_service.edit_project_description(project.id, description=payload.description)
        return project
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete project")
def delete_project(project_id: str, project_service: ProjectService = Depends(get_project_service)) -> None:
    ok = project_service.delete_project(project_id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return None

