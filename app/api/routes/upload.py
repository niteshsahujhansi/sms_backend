from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from uuid import uuid4
from typing import List
from crud.upload_crud import UploadCRUD
from core.database import get_db
from schemas.upload import UploadCreate, UploadResponse, FileUploadRequest
from utils.file_utils import save_and_get_metadata
from utils.constants import FileCategoryEnum

router = APIRouter()

def get_upload_crud(db: Session = Depends(get_db)):
    return UploadCRUD(db)

@router.post("/", response_model= List[UploadResponse])
async def upload_file(
    files: List[UploadFile] = File(...),
    upload_data: FileUploadRequest = Depends(),
    upload_crud: UploadCRUD = Depends(get_upload_crud)
):
    file_category = upload_data.file_category
    related_entity_id = upload_data.related_entity_id

    uploaded_files = []
    for file in files:
        meta = await save_and_get_metadata(file, subdir=file_category)

        upload_create = UploadCreate(
            document_id = uuid4(),
            original_filename = file.filename,
            file_extension = meta['file_extension'],
            content_type = file.content_type,
            file_size = meta['file_size'],
            checksum = meta['checksum'],
            storage_path = meta['storage_path'],
            file_category = file_category,
            related_entity_id = related_entity_id,
            is_active = True,
        )

        uploaded = upload_crud.create_upload_record(upload_create)
        uploaded_files.append(uploaded)

    return uploaded_files


