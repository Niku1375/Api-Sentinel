from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.endpoint import EndpointCreate, EndpointResponse
from app.services.endpoint_service import (
    create_endpoint,
    get_endpoints,
    get_endpoint,
    delete_endpoint
)

from app.core.security import get_current_user
from app.models.user import User


router = APIRouter(prefix="/endpoints", tags=["endpoints"])


@router.post("/", response_model=EndpointResponse)
def add_endpoint(
    endpoint: EndpointCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    result = create_endpoint(db, endpoint, current_user)

    if not result:
        raise HTTPException(status_code=404, detail="Project not found")

    return result


@router.get("/", response_model=list[EndpointResponse])
def list_endpoints(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return get_endpoints(db, current_user)


@router.get("/{endpoint_id}", response_model=EndpointResponse)
def get_single_endpoint(
    endpoint_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    endpoint = get_endpoint(db, endpoint_id, current_user)

    if not endpoint:
        raise HTTPException(status_code=404, detail="Endpoint not found")

    return endpoint


@router.delete("/{endpoint_id}")
def remove_endpoint(
    endpoint_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    endpoint = delete_endpoint(db, endpoint_id, current_user)

    if not endpoint:
        raise HTTPException(status_code=404, detail="Endpoint not found")

    return {"message": "Endpoint deleted"}