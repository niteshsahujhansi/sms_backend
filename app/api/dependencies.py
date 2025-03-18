from fastapi import Depends, HTTPException, Request, status
from itsdangerous import URLSafeSerializer, BadSignature
from core.database import get_db
from models.model import User
from sqlalchemy.orm import Session

SECRET_KEY = "your-secret-key"  # Use the same key as in login
serializer = URLSafeSerializer(SECRET_KEY)

def get_current_user(request: Request, db: Session = Depends(get_db)):
    session_token = request.cookies.get("session")

    if not session_token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        session_data = serializer.loads(session_token)
        user_id = session_data.get("user_id")
    except BadSignature:
        raise HTTPException(status_code=401, detail="Invalid session token")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user  # Return the authenticated user object

def require_role(required_role: str):
    def role_dependency(user=Depends(get_current_user)):
        if user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
            )
        return user  # ✅ Now we return the user object
    return role_dependency

