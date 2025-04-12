import aiofiles
import hashlib
from pathlib import Path
from fastapi import UploadFile
import uuid

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

async def save_and_get_metadata(file: UploadFile, subdir: str = "", algorithm: str = "sha256"):
    ext = Path(file.filename).suffix.lower().lstrip(".")
    unique_name = f"{uuid.uuid4()}.{ext}"
    folder = UPLOAD_DIR / subdir
    folder.mkdir(parents=True, exist_ok=True)
    file_path = folder / unique_name

    size = 0
    hash_func = getattr(hashlib, algorithm)()

    async with aiofiles.open(file_path, "wb") as buffer:
        while chunk := await file.read(1024 * 1024):
            size += len(chunk)
            hash_func.update(chunk)
            await buffer.write(chunk)

    await file.seek(0)
    return {
        "file_extension": ext,
        "storage_path": str(file_path),
        "file_size": size,
        "checksum": hash_func.hexdigest(),
    }
