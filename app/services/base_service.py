from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker, selectinload
from sqlalchemy.exc import IntegrityError
from typing import TypeVar, Generic, Type
from pydantic import BaseModel, EmailStr
from fastapi import HTTPException
from core.database import Base, get_central_db, custom_create_engine
from models.model import Tenant_db_Master

# Generic Type Variables
ModelType = TypeVar("ModelType", bound=[Base])
SchemaType = TypeVar("SchemaType", bound=BaseModel)

class BaseService(Generic[ModelType, SchemaType]):
    def __init__(self, model: Type[ModelType], tenant_id: str = None):
        self.model = model
        if tenant_id:
            db = self.__get_tenant_db(tenant_id=tenant_id)
        else:
            db = get_central_db()
        self.sessionmaker = sessionmaker(bind=db, expire_on_commit=False)  # just store the maker, not session
    
    def __get_tenant_db(self, tenant_id: str):
        central_db = get_central_db()
        SessionLocal = sessionmaker(bind=central_db)
        with SessionLocal() as session:
            tenant = session.query(Tenant_db_Master).filter(Tenant_db_Master.tenant_id == tenant_id).first()
        if tenant:
            return custom_create_engine(user=tenant.db_user, password=tenant.db_password, host=tenant.db_host, port=tenant.db_port, db_name=tenant.db_name)
        else:
            raise ValueError(f"Tenant not found for tenant_id: {tenant_id}")
    
    def validate_email(self, email: EmailStr, model: Type[ModelType] = None) -> None:
        """Validate email format and uniqueness"""
        if email is None:
            return

        with self.sessionmaker() as session:
            # Use the provided model or default to self.model
            model_to_use = model or self.model
            # Check if email already exists
            existing_record = session.query(model_to_use).filter(model_to_use.email == email).first()
            if existing_record:
                raise HTTPException(
                    status_code=400,
                    detail={"email": "Email already registered"}
                )
        
    def get_all(self):
        with self.sessionmaker() as session:
            return session.query(self.model).all()

    def get_by_id(self, obj_id: int):
        with self.sessionmaker() as session:
            return session.query(self.model).filter(self.model.id == obj_id).first()

    def create(self, obj_in: SchemaType):
        with self.sessionmaker() as session:
            db_obj = self.model(**obj_in.model_dump(exclude_unset=True))
            session.add(db_obj)
            try:
                session.commit()
                session.refresh(db_obj)
            except IntegrityError:
                session.rollback()
                raise
            return db_obj

    def update(self, obj_id: int, obj_in: SchemaType):
        with self.sessionmaker() as session:
            db_obj = session.query(self.model).filter(self.model.id == obj_id).first()
            if not db_obj:
                return None
            for key, value in obj_in.model_dump(exclude_unset=True).items():
                setattr(db_obj, key, value)
            session.commit()
            session.refresh(db_obj)
            return db_obj

    def delete(self, obj_id: int):
        with self.sessionmaker() as session:
            db_obj = session.query(self.model).filter(self.model.id == obj_id).first()
            if not db_obj:
                return None
            session.delete(db_obj)
            session.commit()
            return db_obj 