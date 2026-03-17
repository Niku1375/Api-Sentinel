from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])

@router.get("/")
def health_check():
    return {"status": "healthy"}

from fastapi import Depends
from app.core.security import get_current_user
from app.models.user import User


@router.get("/protected")
def protected_route(current_user: User = Depends(get_current_user)):

    return {
        "message": "You are authenticated",
        "user": current_user.email
    }