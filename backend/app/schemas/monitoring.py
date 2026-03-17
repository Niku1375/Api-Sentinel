from pydantic import BaseModel
from datetime import datetime


class MonitoringResultResponse(BaseModel):

    status_code: int | None
    response_time: float
    success: bool
    checked_at: datetime

    class Config:
        from_attributes = True


class MonitoringStats(BaseModel):

    total_checks: int
    successes: int
    failures: int
    uptime_percentage: float
    avg_response_time: float