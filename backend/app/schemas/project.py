from pydantic import BaseModel
from uuid import UUID
class ProjectCreate(BaseModel):

    name: str
    description: str | None = None


class ProjectResponse(BaseModel):

    id: UUID
    name: str
    description: str | None

    class Config:
        from_attributes = True