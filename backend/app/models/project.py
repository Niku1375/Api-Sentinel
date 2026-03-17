import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

from app.database.base import Base


class Project(Base):

    __tablename__ = "projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name = Column(String, nullable=False)

    description = Column(String)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    created_at = Column(DateTime, default=datetime.utcnow)