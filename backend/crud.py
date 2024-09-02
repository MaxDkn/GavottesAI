from backend.auth import get_current_user
from fastapi import APIRouter, Depends
from backend.schemas import User as UserSchema

crud_router = APIRouter()

@crud_router.get('/')
async def home(user: UserSchema = Depends(get_current_user)):
    return {'CRUD message': f'Home {user.username}'}
