from sqlalchemy.orm import Session
from schemas.upload import UploadCreate
from crud.base_crud import CRUDBase
from models.model import Upload
from sqlalchemy.exc import SQLAlchemyError

class UploadCRUD(CRUDBase[Upload, UploadCreate]):
    def __init__(self, db: Session):
        super().__init__(Upload, db)
        
    def create_upload_record(self, obj_in: UploadCreate):
        try:
            file_record = Upload(**obj_in.model_dump())
            self.session.add(file_record)
            self.session.commit()
            self.session.refresh(file_record)
            return file_record
        except SQLAlchemyError as e:
            self.session.rollback()  # Rollback the transaction
            raise Exception(f"Error creating upload record: {str(e)}")

