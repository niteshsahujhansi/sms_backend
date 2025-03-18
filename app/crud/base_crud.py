from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import TypeVar, Generic, Type
from pydantic import BaseModel
from core.database import Base

# Generic Type Variables
ModelType = TypeVar("ModelType", bound=[Base])
SchemaType = TypeVar("SchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, SchemaType]):
    def __init__(self, model: Type[ModelType], db: Session):
        self.model = model
        self.db = db

    def get_all(self):
        return self.db.query(self.model).all()

    def get_by_id(self, obj_id: int):
        return self.db.query(self.model).filter(self.model.id == obj_id).first()

    def create(self, obj_in: SchemaType):
        db_obj = self.model(**obj_in.model_dump())
        self.db.add(db_obj)
        try:
            self.db.commit()
            self.db.refresh(db_obj)
        except IntegrityError:
            self.db.rollback()
            raise
        return db_obj

    def update(self, obj_id: int, obj_in: SchemaType):
        db_obj = self.db.query(self.model).filter(self.model.id == obj_id).first()
        if not db_obj:
            return None
        for key, value in obj_in.model_dump().items():
            setattr(db_obj, key, value)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def delete(self, obj_id: int):
        db_obj = self.db.query(self.model).filter(self.model.id == obj_id).first()
        if not db_obj:
            return None
        self.db.delete(db_obj)
        self.db.commit()
        return db_obj
