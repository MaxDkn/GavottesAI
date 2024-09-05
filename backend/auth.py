from typing import Union
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from backend.models import User
from backend.database import get_db
from backend.schemas import UserCreate, User as UserSchema, UserResponse

SECRET_KEY = "967f22d0881ab29b5809974b93b457f0"  # Remplace par une clé plus sécurisée
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
auth_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/get_user_token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user


# Créer un utilisateur
@auth_router.post("/create_user", response_model=UserSchema)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Nom d'Utilisateur déjà pris. Veuillez en choisir un autre.")
    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Générer un token d'accès
@auth_router.post("/get_user_token", response_model=dict)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


# Route sécurisée pour obtenir les infos de l'utilisateur actuel
@auth_router.get("/me", response_model=UserResponse)
def read_users_me(current_user: UserSchema = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(User).filter(User.id==current_user.id).first()

@auth_router.get('/all', response_model=list[UserResponse])
def all_users(db: Session = Depends(get_db)): 
    return db.query(User).all()
