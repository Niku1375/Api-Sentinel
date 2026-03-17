from sqlalchemy.orm import Session

from app.models.endpoint import Endpoint
from app.schemas.endpoint import EndpointCreate
from app.models.user import User
from app.models.project import Project


def create_endpoint(db: Session, endpoint: EndpointCreate, user: User):

    project = db.query(Project).filter(
        Project.id == endpoint.project_id,
        Project.user_id == user.id
    ).first()

    if not project:
        return None

    db_endpoint = Endpoint(
        project_id=endpoint.project_id,
        name=endpoint.name,
        url=endpoint.url,
        method=endpoint.method,
        interval_seconds=endpoint.interval_seconds,
        timeout_seconds=endpoint.timeout_seconds
    )

    db.add(db_endpoint)
    db.commit()
    db.refresh(db_endpoint)

    return db_endpoint


def get_endpoints(db: Session, user: User):

    return db.query(Endpoint).join(Project).filter(
        Project.user_id == user.id
    ).all()


def get_endpoint(db: Session, endpoint_id: str, user: User):

    return db.query(Endpoint).join(Project).filter(
        Endpoint.id == endpoint_id,
        Project.user_id == user.id
    ).first()


def delete_endpoint(db: Session, endpoint_id: str, user: User):

    endpoint = get_endpoint(db, endpoint_id, user)

    if not endpoint:
        return None

    db.delete(endpoint)
    db.commit()

    return endpoint