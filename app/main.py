from fastapi import FastAPI
from api.routes.students import router as student_router
from api.routes.parents import router as parent_router
from api.routes.auth import router as auth_router
from api.routes.users import router as user_router
from api.routes.upload import router as upload_router
from fastapi.middleware.cors import CORSMiddleware
from core.database import init_db
# from core.exceptions import api_exception_handler, APIException

app = FastAPI()

init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# app.add_exception_handler(APIException, api_exception_handler)

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(user_router, prefix="/user", tags=["User"])
app.include_router(student_router, prefix="/students", tags=["Students"])
app.include_router(parent_router, prefix="/parents", tags=["Parents"])
app.include_router(upload_router, prefix="/upload", tags=["upload"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
