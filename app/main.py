from fastapi import FastAPI
from api.routes.students import router as student_router
from api.routes.parents import router as parent_router
from api.routes.upload import router as upload_router
from api.routes.teachers import router as teacher_router
from fastapi.middleware.cors import CORSMiddleware
from core.database import init_db
# from core.exceptions import api_exception_handler, APIException

app = FastAPI()

init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Update this for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# app.add_exception_handler(APIException, api_exception_handler)

app.include_router(student_router, prefix="/students", tags=["Students"])
app.include_router(parent_router, prefix="/parents", tags=["Parents"])
app.include_router(upload_router, prefix="/upload", tags=["upload"])
app.include_router(teacher_router, prefix="/teachers", tags=["Teachers"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
