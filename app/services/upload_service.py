from sqlalchemy.orm import Session
from schemas.upload import UploadCreate
from services.base_service import BaseService
from models.model import Upload
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

class UploadService(BaseService[Upload, UploadCreate]):
    def __init__(self, tenant_id: str):
        super().__init__(Upload, tenant_id)
        
    def create_upload_record(self, obj_in: UploadCreate):
        try:
            with self.sessionmaker() as session:
                file_record = Upload(**obj_in.model_dump())
                session.add(file_record)
                session.commit()
                session.refresh(file_record)
                return file_record
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error creating upload record: {str(e)}"
            ) 