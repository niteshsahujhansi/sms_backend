from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from typing import TypeVar, Generic, Type
from pydantic import BaseModel
from core.database import Base, get_central_db, custom_create_engine
from models.model import Tenant_db_Master

# Generic Type Variables
ModelType = TypeVar("ModelType", bound=[Base])
SchemaType = TypeVar("SchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, SchemaType]):
    def __init__(self, model: Type[ModelType], tenant_id: str = None):
        self.model = model
        if tenant_id:
            db = self.__get_tenant_db(tenant_id=tenant_id)
        else:
            db = get_central_db()
        self.session = sessionmaker(bind=db)()
    
    def __get_tenant_db(self, tenant_id: str):
        central_db = get_central_db()
        session = sessionmaker(bind=central_db)()
        tenant = session.query(Tenant_db_Master).filter(Tenant_db_Master.tenant_id == tenant_id).first()
        if tenant:
            return custom_create_engine(user=tenant.db_user, password=tenant.db_password, host=tenant.db_host, port=tenant.db_port, db_name=tenant.db_name)
        
    def get_all(self):
        return self.session.query(self.model).all()

    def get_by_id(self, obj_id: int):
        return self.session.query(self.model).filter(self.model.id == obj_id).first()

    def create(self, obj_in: SchemaType):
        db_obj = self.model(**obj_in.model_dump(exclude_unset=True))
        self.session.add(db_obj)
        try:
            self.session.commit()
            self.session.refresh(db_obj)
        except IntegrityError:
            self.session.rollback()
            raise
        return db_obj

    def update(self, obj_id: int, obj_in: SchemaType):
        db_obj = self.session.query(self.model).filter(self.model.id == obj_id).first()
        if not db_obj:
            return None
        for key, value in obj_in.model_dump(exclude_unset=True).items():
            setattr(db_obj, key, value)
        self.session.commit()
        self.session.refresh(db_obj)
        return db_obj

    def delete(self, obj_id: int):
        db_obj = self.session.query(self.model).filter(self.model.id == obj_id).first()
        if not db_obj:
            return None
        self.session.delete(db_obj)
        self.session.commit()
        return db_obj
