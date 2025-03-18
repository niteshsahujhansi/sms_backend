from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.dependencies import require_role
from core.database import get_db
from models.model import User
from schemas.user import UserResponse

router = APIRouter()

@router.get("/me", response_model=UserResponse)
def get_current_user_data(current_user: User = Depends(require_role("a"))):
    print(f"User {current_user.username} (Role: {current_user.role}) accessed /students")
    return current_user
    # return {"message": f"Hello {current_user.username}, here is the student list"}
