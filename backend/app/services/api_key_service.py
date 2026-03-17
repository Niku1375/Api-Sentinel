import uuid
import secrets
import hashlib
from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.api_key import APIKey
from app.schemas.api_key import APIKeyCreate


def _generate_raw_key() -> str:
    """
    Creates a cryptographically secure key.
    'sk_' prefix makes it recognizable (like Stripe's sk_live_ pattern).
    token_urlsafe(32) gives 256 bits of entropy — unguessable.
    """
    return "sk_" + secrets.token_urlsafe(32)


def _hash_key(raw_key: str) -> str:
    """
    SHA-256 is appropriate here because the key is already high-entropy.
    bcrypt would be overkill and slow for every API request verification.
    """
    return hashlib.sha256(raw_key.encode()).hexdigest()


def create_api_key(db: Session, user_id: str, data: APIKeyCreate):
    """
    Generates key, hashes it, stores hash.
    Returns (db_record, raw_key) — caller must return raw_key to user immediately.
    """
    raw_key = _generate_raw_key()
    key_hash = _hash_key(raw_key)
    key_hint = raw_key[-4:]   # last 4 chars of the raw key

    db_key = APIKey(
        id=uuid.uuid4(),
        user_id=user_id,
        name=data.name,
        key_hash=key_hash,
        key_hint=key_hint,
        is_active=True,
        created_at=datetime.now(timezone.utc)
    )

    db.add(db_key)
    db.commit()
    db.refresh(db_key)

    return db_key, raw_key   # raw_key returned here, never stored


def list_api_keys(db: Session, user_id: str):
    """Returns all active keys for this user — no raw keys, just metadata."""
    return (
        db.query(APIKey)
        .filter(APIKey.user_id == user_id, APIKey.is_active == True)
        .order_by(APIKey.created_at.desc())
        .all()
    )


def revoke_api_key(db: Session, key_id: str, user_id: str):
    """
    Hard deletes the key. User must own it — prevents one user revoking another's key.
    """
    key = db.query(APIKey).filter(
        APIKey.id == key_id,
        APIKey.user_id == user_id
    ).first()

    if not key:
        raise HTTPException(status_code=404, detail="API key not found")

    db.delete(key)
    db.commit()

    return {"message": "API key revoked successfully"}


def verify_api_key(db: Session, raw_key: str):
    """
    Hashes the incoming key and looks it up.
    Updates last_used_at on success — useful for auditing unused keys.
    Returns the key record (with user_id) or None if invalid.
    """
    key_hash = _hash_key(raw_key)

    key = db.query(APIKey).filter(
        APIKey.key_hash == key_hash,
        APIKey.is_active == True
    ).first()

    if not key:
        return None

    # Track last usage — helps user identify stale/unused keys
    key.last_used_at = datetime.now(timezone.utc)
    db.commit()

    return key