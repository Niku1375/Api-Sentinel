import uuid
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

from app.database.base import Base


class MonitorResult(Base):

    __tablename__ = "monitor_results"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    endpoint_id = Column(UUID(as_uuid=True), ForeignKey("endpoints.id"))

    status_code = Column(Integer)

    response_time = Column(Float)

    success = Column(Boolean)

    checked_at = Column(DateTime, default=datetime.utcnow)