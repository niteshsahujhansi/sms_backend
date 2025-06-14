from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.parent import ParentCreate, ParentResponse, ParentUpdate, ParentResponseMessage
from services.parent_service import ParentService
from api.dependencies import require_roles
from schemas.common_schemas import UserToken

router = APIRouter()

@router.get("/", response_model=list[ParentResponse])
def read_parents(current_user: UserToken = Depends(require_roles("admin", "teacher"))):
    parent_service = ParentService(current_user.tenant_id)
    return parent_service.get_all()

@router.get("/{parent_id}", response_model=ParentResponse)
def read_parent(parent_id: int
                , current_user: UserToken = Depends(require_roles("admin"))
                ):
    parent_service = ParentService(current_user.tenant_id)
    parent = parent_service.get_by_id(parent_id)
    if not parent:
        raise HTTPException(status_code=404, detail="Parent not found")
    return parent


@router.post("/", response_model=ParentResponseMessage)
# @router.post("/", response_model=ParentResponse)
def create_new_parent(parent: ParentCreate, current_user: UserToken = Depends(require_roles("admin"))):
    parent_service = ParentService(current_user.tenant_id)
    parent = parent_service.create(parent)
    # return parent
    return {"id":parent.id, "message": "Parent created successfully"}


@router.put("/{parent_id}", response_model=ParentResponse)
def update_parent(parent_id: int, parent: ParentUpdate, current_user: UserToken = Depends(require_roles("admin"))):
    parent_service = ParentService(current_user.tenant_id)
    updated_parent = parent_service.update(parent_id, parent)
    if not updated_parent:
        raise HTTPException(status_code=404, detail="Parent not found")
    return updated_parent


@router.delete("/{parent_id}")
def delete_parent(parent_id: int, current_user: UserToken = Depends(require_roles("admin"))):
    parent_service = ParentService(current_user.tenant_id)
    deleted_parent = parent_service.delete(parent_id)
    if not deleted_parent:
        raise HTTPException(status_code=404, detail="Parent not found")
    return {"message": "Parent deleted successfully"}