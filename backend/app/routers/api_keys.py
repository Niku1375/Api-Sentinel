from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.api_key import (
    APIKeyCreate,
    APIKeyResponse,
    APIKeyCreatedResponse,
    APIKeyVerifyRequest,
    APIKeyVerifyResponse
)
from app.services.api_key_service import (
    create_api_key,
    list_api_keys,
    revoke_api_key,
    verify_api_key
)


router = APIRouter(prefix="/api-keys", tags=["api-keys"])


@router.post("/", response_model=APIKeyCreatedResponse)
def create_key(
    data: APIKeyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Creates a new API key.
    The raw key is returned ONCE here and never retrievable again.
    User should copy it immediately.
    """
    db_key, raw_key = create_api_key(db, current_user.id, data)

    # Build response manually — raw_key isn't on the model, we attach it here
    return APIKeyCreatedResponse(
        id=db_key.id,
        name=db_key.name,
        key_hint=db_key.key_hint,
        is_active=db_key.is_active,
        created_at=db_key.created_at,
        last_used_at=db_key.last_used_at,
        raw_key=raw_key   # One-time exposure
    )


@router.get("/", response_model=List[APIKeyResponse])
def get_keys(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lists all active API keys for the current user. Never exposes raw keys."""
    return list_api_keys(db, current_user.id)


@router.delete("/{key_id}")
def revoke_key(
    key_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Permanently deletes a key. Cannot be undone."""
    return revoke_api_key(db, key_id, current_user.id)


@router.post("/verify", response_model=APIKeyVerifyResponse)
def verify_key(
    payload: APIKeyVerifyRequest,
    db: Session = Depends(get_db)
):
    """
    No auth required — this is FOR external services authenticating themselves.
    Returns valid=True + user_id if the key is recognized, valid=False otherwise.
    """
    key_record = verify_api_key(db, payload.key)

    if not key_record:
        return APIKeyVerifyResponse(valid=False)

    return APIKeyVerifyResponse(valid=True, user_id=key_record.user_id)