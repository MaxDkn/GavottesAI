from fastapi import FastAPI
from backend.auth import auth_router
from backend.crud import crud_router

app = FastAPI()
app.include_router(auth_router, prefix="/auth", tags=['auth'])
app.include_router(crud_router, prefix="/house", tags=['house'])

@app.get('/')
async def test():
    return {'Hello': 'World'}