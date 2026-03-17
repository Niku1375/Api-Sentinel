from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.core.security import get_current_user
from app.models.user import User

from app.services.monitoring_service import (
    get_monitoring_history,
    get_monitoring_stats,
    get_incidents
)

from app.schemas.monitoring import MonitoringResultResponse, MonitoringStats


router = APIRouter(prefix="/monitoring", tags=["monitoring"])


@router.get("/history/{endpoint_id}", response_model=list[MonitoringResultResponse])
def history(
    endpoint_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return get_monitoring_history(db, endpoint_id, current_user)


@router.get("/stats/{endpoint_id}", response_model=MonitoringStats)
def stats(
    endpoint_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return get_monitoring_stats(db, endpoint_id, current_user)


@router.get("/incidents/{endpoint_id}", response_model=list[MonitoringResultResponse])
def incidents(
    endpoint_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return get_incidents(db, endpoint_id, current_user)