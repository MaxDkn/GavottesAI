from backend.schemas import User as UserSchema, HouseCreate, HouseResponse, GetHouseID, EditHouse
from backend.auth import get_current_user
from fastapi import APIRouter, Depends, HTTPException, status
from backend.database import get_db
from sqlalchemy.orm import Session
from backend.models import House
#  Database => db: Session = Depends(get_db)
#  User login => user: UserSchema = Depends(get_current_user)



crud_router = APIRouter()


@crud_router.get('/all', response_model=list[HouseResponse])
async def all_houses_in_the_database(db: Session = Depends(get_db)):
    return db.query(House).all()


@crud_router.get('/me', response_model=list[HouseResponse])
async def all_houses_of_user(user: UserSchema = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(House).filter(House.SellerID==user.id).all()


@crud_router.post('/create', response_model=HouseResponse)
async def create_house(house: HouseCreate, user: UserSchema = Depends(get_current_user), db: Session = Depends(get_db)):
    db_house = House(**house.dict(), SellerID=user.id)
    db.add(db_house)
    db.commit()
    db.refresh(db_house)
    return db_house


@crud_router.get('/{house_id}', response_model=HouseResponse)
async def specific_house(house_id: int, db: Session = Depends(get_db)):
    stored_house = db.query(House).filter(House.id==house_id).first()
    if not stored_house:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"House with ID {house_id} not found the database")
    return stored_house

@crud_router.patch('/edit', response_model=HouseResponse)
async def modify_house(house: EditHouse, user: UserSchema = Depends(get_current_user), db: Session = Depends(get_db)):
    stored_house = db.query(House).filter(House.id==house.id and House.SellerID==user.id).first()
    if not stored_house:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"House with ID {house.id} not found in {user.username.title()}'s dataset")
    update_data = house.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(stored_house, key, value)
    db.commit()
    db.refresh(stored_house)
    return db.query(House).filter(House.id==house.id and House.SellerID==user.id).first()

#  Get all houses => /house/all
#  Get all my houses => /house/me
#  Get specific house => /house/{id}

@crud_router.delete('/delete', response_model=dict)
async def delete_house(house: GetHouseID, user: UserSchema = Depends(get_current_user), db: Session = Depends(get_db)):
    stored_house = db.query(House).filter(House.id==house.id and House.SellerID==user.id).first()
    if not stored_house:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"House with ID {house.id} not found in {user.username.title()}'s dataset")
    db.delete(stored_house)
    db.commit()
    return {"msg": f"House {house.id} deleted without problems!"}
