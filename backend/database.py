from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.models import Base

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crée la base de données si elle n'existe pas
Base.metadata.create_all(bind=engine)

# Dépendance pour la session de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
