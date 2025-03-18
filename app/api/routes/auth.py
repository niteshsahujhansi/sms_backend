from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from itsdangerous import URLSafeSerializer
from utils.security import verify_password, hash_password
from core.database import get_db
from models.model import User
from schemas.user import UserLogin

router = APIRouter()

SECRET_KEY = "your-secret-key"  # Change this to a secure key
serializer = URLSafeSerializer(SECRET_KEY)

@router.post("/login")
def login(user_data: UserLogin, response: Response, db: Session = Depends(get_db)):
    # Fetch user from DB
    user = db.query(User).filter(User.username == user_data.username).first()
    
    # if not user or not verify_password(user_data.password, user.hashed_password):
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Generate session token
    session_token = serializer.dumps({"user_id": user.id, "role": user.role})

    # Set HTTP-only session cookie
    response.set_cookie(
        key="session",
        value=session_token,
        httponly=True,
        max_age=3600  # 1 hour expiry
    )

    return {"message": "Login successful"}

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("session")  # Remove session cookie
    return {"message": "Logged out successfully"}