from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.alert import Alert
from app.models.endpoint import Endpoint
from app.models.project import Project


router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("/")
def get_alerts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    alerts = db.query(Alert).join(Endpoint).join(Project).filter(
        Project.user_id == current_user.id
    ).all()

    return alerts