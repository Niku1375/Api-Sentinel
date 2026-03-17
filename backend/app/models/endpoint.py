import uuid
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

from app.database.base import Base


class Endpoint(Base):

    __tablename__ = "endpoints"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"))

    name = Column(String, nullable=False)

    url = Column(String, nullable=False)

    method = Column(String, default="GET")

    interval_seconds = Column(Integer, default=60)

    timeout_seconds = Column(Integer, default=5)

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    
    alert_active = Column(Boolean, default=False)