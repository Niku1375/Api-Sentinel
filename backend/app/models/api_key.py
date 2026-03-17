import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, ForeignKey, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID

from app.database.base import Base


class APIKey(Base):

    __tablename__ = "api_keys"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    # Human-readable label — e.g. "Production server", "CI pipeline"
    name = Column(String, nullable=False)

    # SHA-256 hash of the raw key — never store plaintext
    key_hash = Column(String, unique=True, nullable=False)

    # Last 4 chars of the raw key — safe to store, helps user identify keys
    key_hint = Column(String(4), nullable=False)

    # Allows soft-disabling without deletion (useful later)
    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Updated every time this key is used to authenticate
    last_used_at = Column(DateTime(timezone=True), nullable=True)