from fastapi import FastAPI
from backend.auth import auth_router
from backend.crud import crud_router
from backend.frontend import frontend_router

app = FastAPI()
app.include_router(auth_router, prefix="/api/auth", tags=['auth'])
app.include_router(crud_router, prefix="/api/house", tags=['house'])
app.include_router(frontend_router, prefix="", tags=['frontend'])
