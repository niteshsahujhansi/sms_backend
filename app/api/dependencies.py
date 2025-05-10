from fastapi import Depends, HTTPException, status, Cookie
from sqlalchemy.orm import Session
from typing import Optional
from models.model import UserMaster
from schemas.common_schemas import UserToken
from crud.base_crud import CRUDBase
from utils.security import verify_access_token

# def get_user_master_crud():
#     return CRUDBase()

async def get_current_user(access_token: Optional[str] = Cookie(None)) -> UserToken:
    if access_token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing access token")

    payload = verify_access_token(access_token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user_id: int = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token missing subject (sub)")

    user_master_crud = CRUDBase(UserMaster)
    user = user_master_crud.get_by_id(obj_id=user_id)
    # user = db.query(UserMaster).filter(UserMaster.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    # Map ORM model to schema
    return UserToken.model_validate(user)

def require_roles(*roles: str):
    def role_guard(UserToken: UserToken = Depends(get_current_user)) -> UserToken:
        if UserToken.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Required roles: {', '.join(roles)}"
            )
        return UserToken
    return role_guard



