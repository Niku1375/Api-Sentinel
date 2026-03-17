from sqlalchemy.orm import Session
from app.models.alert import Alert
from app.models.monitor_result import MonitorResult

FAILURE_THRESHOLD = 3


def check_failure_threshold(db: Session, endpoint_id: str) -> bool:
    """
    Returns True if the last FAILURE_THRESHOLD checks for this endpoint
    have all failed. Otherwise, False.
    """
    recent_checks = (
        db.query(MonitorResult)
        .filter(MonitorResult.endpoint_id == endpoint_id)
        .order_by(MonitorResult.checked_at.desc())
        .limit(FAILURE_THRESHOLD)
        .all()
    )

    if len(recent_checks) < FAILURE_THRESHOLD:
        return False

    # True if all last N results failed
    return all(not r.success for r in recent_checks)


def create_alert(db: Session, endpoint_id: str, message: str) -> Alert:
    """
    Creates and saves an alert record in the database.
    """
    alert = Alert(endpoint_id=endpoint_id, message=message)
    db.add(alert)
    db.commit()
    db.refresh(alert)  # refresh to get updated object (optional but good practice)
    return alert