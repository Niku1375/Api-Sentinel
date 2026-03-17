import uuid
from sqlalchemy import Column, DateTime, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

from app.database.base import Base


class Alert(Base):

    __tablename__ = "alerts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    endpoint_id = Column(UUID(as_uuid=True), ForeignKey("endpoints.id"))

    message = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)