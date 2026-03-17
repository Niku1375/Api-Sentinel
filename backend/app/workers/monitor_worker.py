import time
import httpx
import asyncio
from app.websocket.connection_manager import manager
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.models.endpoint import Endpoint
from app.models.monitor_result import MonitorResult
from app.models.project import Project
from app.models.user import User
from app.services.alert_service import check_failure_threshold, create_alert
from app.services.notification_service import send_email_alert


async def check_endpoint(endpoint_id):
    """
    Check a single endpoint, record result, send alert or recovery if needed.
    """

    db: Session = SessionLocal()
    # Refetch fresh endpoint from DB to get updated alert_active state
    endpoint = db.query(Endpoint).filter(Endpoint.id == endpoint_id).first()
    if not endpoint or not endpoint.is_active:
        db.close()
        return

    start = time.time()
    success = False
    status_code = None

    try:
        async with httpx.AsyncClient(timeout=endpoint.timeout_seconds) as client:
            response = await client.request(endpoint.method, endpoint.url)
            status_code = response.status_code
            if status_code < 500:
                success = True
    except Exception:
        success = False

    response_time = (time.time() - start) * 1000

    # Record monitoring result
    result = MonitorResult(
        endpoint_id=endpoint.id,
        status_code=status_code,
        response_time=response_time,
        success=success
    )
    db.add(result)
    db.commit()


    await manager.broadcast({
        "endpoint_id": str(endpoint.id),
        "endpoint_name": endpoint.name,
        "status_code": status_code,
        "response_time": response_time,
        "success": success
    })

    # -----------------------------
    # ALERT LOGIC
    # -----------------------------

    # Fetch project and user once
    project = db.query(Project).filter(Project.id == endpoint.project_id).first()
    user = None
    if project:
        user = db.query(User).filter(User.id == project.user_id).first()

    # Case 1 — failure
    if not success:
        threshold_reached = check_failure_threshold(db, endpoint.id)
        if threshold_reached and not endpoint.alert_active:
            # Create alert
            alert = create_alert(
                db,
                endpoint.id,
                f"Endpoint {endpoint.name} failed 3 consecutive checks"
            )

            # Send email alert
            if user:
                try:
                    send_email_alert(user.email, "API Sentinel Alert", alert.message)
                except Exception as e:
                    print("Email sending failed:", e)

            # Mark alert active
            endpoint.alert_active = True
            db.commit()

    # Case 2 — recovery
    else:
        if endpoint.alert_active:
            # Send recovery email
            if user:
                try:
                    send_email_alert(
                        user.email,
                        "API Sentinel Recovery",
                        f"Endpoint {endpoint.name} is back UP"
                    )
                except Exception as e:
                    print("Recovery email failed:", e)

            # Reset alert state
            endpoint.alert_active = False
            db.commit()

    db.close()


async def run_monitoring():
    db = SessionLocal()
    # Fetch all active endpoints
    endpoints = db.query(Endpoint).filter(Endpoint.is_active == True).all()
    db.close()

    tasks = [check_endpoint(e.id) for e in endpoints]
    await asyncio.gather(*tasks)


