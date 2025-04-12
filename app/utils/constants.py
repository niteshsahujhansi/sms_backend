

from enum import Enum

class RelatedEntityEnum(str, Enum):
    user = "user"                      # student, teacher, parent, admin
    homework = "homework"
    exam = "exam"
    class_group = "class"
    subject = "subject"
    academic_year = "academic_year"
    notice = "notice"
    event = "event"
    fee_payment = "fee_payment"
    transport = "transport"
    medical_record = "medical_record"
    circular = "circular"
    system = "system"
    unknown = "unknown"

class FileCategoryEnum(str, Enum):
    profile_picture = "profile_picture"
    id_proof = "id_proof"
    assignment = "assignment"
    marksheet = "marksheet"
    certificate = "certificate"
    fee_receipt = "fee_receipt"
    result_sheet = "result_sheet"
    circular_document = "circular_document"
    syllabus_document = "syllabus_document"
    homework_attachment = "homework_attachment"
    invoice = "invoice"
    general_document = "general_document"
    temporary_upload = "temporary_upload"
    miscellaneous = "miscellaneous"

class FileTypeEnum(str, Enum):
    image = "image"
    pdf = "pdf"
    excel = "excel"
    document = "document"
    audio = "audio"
    video = "video"
    other = "other"
    unknown = "unknown"

class UserRoleEnum(str, Enum):
    student = "student"
    teacher = "teacher"
    parent = "parent"
    admin = "admin"
    system = "system"  # optional
    unknown = "unknown"

class FileStatusEnum(str, Enum):
    archived = "archived"
    deleted = "deleted"
    pending = "pending"
    failed = "failed"

class VirusScanStatusEnum(str, Enum):
    pending = "pending"
    clean = "clean"
    infected = "infected"
    failed = "failed"
    skipped = "skipped"

class ContentTypeEnum(str, Enum):
    jpeg = "image/jpeg"
    png = "image/png"
    svg = "image/svg+xml"
    pdf = "application/pdf"
    doc = "application/msword"
    docx = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    xls = "application/vnd.ms-excel"
    xlsx = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    ppt = "application/vnd.ms-powerpoint"
    pptx = "application/vnd.openxmlformats-officedocument.presentationml.presentation"
    rtf = "application/rtf"
    txt = "text/plain"
    csv = "text/csv"
    json = "application/json"
    xml = "application/xml"
    mp3 = "audio/mpeg"
    mp4 = "video/mp4"
    zip = "application/zip"
    unknown = "application/octet-stream"

class FileExtensionEnum(str, Enum):
    jpg = "jpg"
    jpeg = "jpeg"
    png = "png"
    svg = "svg"
    pdf = "pdf"
    doc = "doc"
    docx = "docx"
    xls = "xls"
    xlsx = "xlsx"
    ppt = "ppt"
    pptx = "pptx"
    rtf = "rtf"
    txt = "txt"
    csv = "csv"
    json = "json"
    xml = "xml"
    mp3 = "mp3"
    mp4 = "mp4"
    zip = "zip"
    unknown = "unknown"
