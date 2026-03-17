from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.monitor_result import MonitorResult
from app.models.endpoint import Endpoint
from app.models.project import Project
from app.models.user import User
import json
from app.core.cache import cache_get, cache_set


def get_monitoring_history(db: Session, endpoint_id: str, user: User):
    return db.query(MonitorResult).join(Endpoint).join(Project).filter(
        MonitorResult.endpoint_id == endpoint_id,
        Project.user_id == user.id
    ).order_by(MonitorResult.checked_at.desc()).limit(50).all()


def get_monitoring_stats(db: Session, endpoint_id: str, user: User):
    # Try cache first
    cache_key = f"stats:{endpoint_id}"
    cached = cache_get(cache_key)
    if cached:
        return json.loads(cached)

    # Query with user permission check
    results = db.query(MonitorResult).join(Endpoint).join(Project).filter(
        MonitorResult.endpoint_id == endpoint_id,
        Project.user_id == user.id
    )

    total_checks = results.count()
    successes = results.filter(MonitorResult.success == True).count()
    failures = results.filter(MonitorResult.success == False).count()

    avg_latency = db.query(func.avg(MonitorResult.response_time)).filter(
        MonitorResult.endpoint_id == endpoint_id
    ).scalar()

    uptime = (successes / total_checks) * 100 if total_checks > 0 else 0

    stats = {
        "total_checks": total_checks,
        "successes": successes,
        "failures": failures,
        "uptime_percentage": round(uptime, 2),
        "avg_response_time": round(avg_latency or 0, 2)
    }

    # Save to cache
    cache_set(cache_key, json.dumps(stats), ttl=30)

    return stats


def get_incidents(db: Session, endpoint_id: str, user: User):
    return db.query(MonitorResult).join(Endpoint).join(Project).filter(
        MonitorResult.endpoint_id == endpoint_id,
        MonitorResult.success == False,
        Project.user_id == user.id
    ).order_by(MonitorResult.checked_at.desc()).limit(20).all()