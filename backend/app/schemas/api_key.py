from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional


class APIKeyCreate(BaseModel):
    # User just provides a label — we generate the key
    name: str


class APIKeyResponse(BaseModel):
    id: UUID
    name: str
    key_hint: str       # e.g. "xQ3z" — last 4 chars, safe to show
    is_active: bool
    created_at: datetime
    last_used_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class APIKeyCreatedResponse(APIKeyResponse):
    # Extends the base response — only returned ONCE at creation
    raw_key: str        # e.g. "sk_abc123...xyz" — show once, never stored


class APIKeyVerifyRequest(BaseModel):
    key: str            # The raw key provided by external caller


class APIKeyVerifyResponse(BaseModel):
    valid: bool
    user_id: Optional[UUID] = None   # Returned so the caller knows who owns it