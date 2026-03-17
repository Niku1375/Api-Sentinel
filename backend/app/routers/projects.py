from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.project import ProjectCreate, ProjectResponse
from app.services.project_service import (
    create_project,
    get_projects,
    get_project,
    delete_project
)

from app.core.security import get_current_user
from app.models.user import User


router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("/", response_model=ProjectResponse)
def create_new_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return create_project(db, project, current_user)


@router.get("/", response_model=list[ProjectResponse])
def list_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return get_projects(db, current_user)


@router.get("/{project_id}", response_model=ProjectResponse)
def get_single_project(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    project = get_project(db, project_id, current_user)

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return project


@router.delete("/{project_id}")
def remove_project(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    project = delete_project(db, project_id, current_user)

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return {"message": "Project deleted"}