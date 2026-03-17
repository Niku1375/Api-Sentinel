from pydantic import BaseModel
from uuid import UUID

class EndpointCreate(BaseModel):

    project_id: UUID
    name: str
    url: str
    method: str = "GET"
    interval_seconds: int = 60
    timeout_seconds: int = 5


class EndpointResponse(BaseModel):

    id: UUID
    name: str
    url: str
    method: str
    interval_seconds: int
    timeout_seconds: int

    class Config:
        from_attributes = True