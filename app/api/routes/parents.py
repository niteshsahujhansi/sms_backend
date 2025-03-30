from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from schemas.parent import ParentCreate, ParentResponse, ParentUpdate
from crud.parent_crud import ParentCRUD

router = APIRouter()

# ✅ Dependency injection to get `ParentCRUD`
def get_parent_crud(db: Session = Depends(get_db)):
    return ParentCRUD(db)

@router.get("/", response_model=list[ParentResponse])
def read_parents(parent_crud: ParentCRUD = Depends(get_parent_crud)):
    return parent_crud.get_all()

@router.get("/{parent_id}", response_model=ParentResponse)
# def read_parent(parent_id: UUID, parent_crud: ParentCRUD = Depends(get_parent_crud)):
def read_parent(parent_id: int, parent_crud: ParentCRUD = Depends(get_parent_crud)):
    parent = parent_crud.get_by_id(parent_id)
    if not parent:
        raise HTTPException(status_code=404, detail="Parent not found")
    return parent

@router.post("/", response_model=ParentResponse)
def create_new_parent(parent: ParentCreate, parent_crud: ParentCRUD = Depends(get_parent_crud)):
    return parent_crud.create(parent)

@router.put("/{parent_id}", response_model=ParentResponse)
def update_parent(parent_id: int, parent: ParentUpdate, parent_crud: ParentCRUD = Depends(get_parent_crud)):
    updated_parent = parent_crud.update(parent_id, parent)
    if not updated_parent:
        raise HTTPException(status_code=404, detail="Parent not found")
    return updated_parent

@router.delete("/{parent_id}")
def delete_parent(parent_id: int, parent_crud: ParentCRUD = Depends(get_parent_crud)):
    deleted_parent = parent_crud.delete(parent_id)
    if not deleted_parent:
        raise HTTPException(status_code=404, detail="Parent not found")
    return {"message": "Parent deleted successfully"}