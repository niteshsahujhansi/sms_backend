from pydantic import BaseModel, Field, HttpUrl
from typing import Optional
from uuid import UUID
from datetime import datetime, timedelta, timezone
from utils.constants import RelatedEntityEnum, FileCategoryEnum, FileTypeEnum, UserRoleEnum, FileStatusEnum, VirusScanStatusEnum, ContentTypeEnum, FileExtensionEnum

class BaseUpload(BaseModel):
    document_id: UUID
    original_filename: str
    file_extension: FileExtensionEnum
    content_type: ContentTypeEnum
    file_size: int
    checksum: str
    storage_path: str
    file_category: FileCategoryEnum = FileCategoryEnum.miscellaneous
    file_type: FileTypeEnum = FileTypeEnum.other
    url: Optional[HttpUrl] = None
    expiry_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc) + timedelta(days=30))
    is_private: bool = True
    status: FileStatusEnum = FileStatusEnum.archived
    virus_scan_status: VirusScanStatusEnum = VirusScanStatusEnum.pending
    related_entity: RelatedEntityEnum = RelatedEntityEnum.unknown
    related_entity_id: int
    related_entity_role: UserRoleEnum = UserRoleEnum.unknown
    is_active: Optional[bool] = False
    is_deleted: Optional[bool] = False
    # uploaded_by_id: Optional[UUID]
    # uploaded_by_role: Optional[UserRoleEnum] = UserRoleEnum.unknown
    # updated_by_id: Optional[UUID]
    # updated_by_role: Optional[UserRoleEnum] = UserRoleEnum.unknown

class UploadCreate(BaseUpload):
    pass

class UploadResponse(BaseUpload):
    pass

class FileUploadRequest(BaseModel):
    file_category: FileCategoryEnum = Field(..., description="The category of the file being uploaded")
    related_entity_id: int = Field(..., description="ID of the related entity")
