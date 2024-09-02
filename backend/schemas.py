# schemas.py
from pydantic import BaseModel
import datetime
from typing import Optional


#  User
class UserCreate(BaseModel):
    username: str
    password: str

class User(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True

class UserResponse(User):
    id: int
    username: str
    hashed_password: str

    class Config:
        from_attributes = True

#  House
from pydantic import BaseModel
import datetime

# Classe de base avec les attributs communs
class HouseBase(BaseModel):
    AddressNumber: int
    StreetName: str
    Respond: bool
    Size: str
    SecurityGameOrAlarm: bool
    Dog: str
    Age: str
    Gender: str
    Price: float

    class Config:
        extra = "forbid"

# Classe pour la création de maison, hérite de HouseBase
class HouseCreate(HouseBase):
    pass

# Classe pour la réponse avec des attributs supplémentaires
class HouseResponse(HouseBase):
    id: int
    SellerID: int
    AddressNumber: int
    StreetName: str
    DayTime: datetime.datetime
    Respond: bool
    Size: str
    SecurityGameOrAlarm: bool
    Dog: str
    Age: str
    Gender: str
    Price: float
    
    class Config:
        from_attributes = True


# Classe pour obtenir l'identifiant d'une maison
class GetHouseID(BaseModel):
    id: int

    class Config:
        from_attributes = True
        extra = 'forbid'


class EditHouse(GetHouseID):
    AddressNumber: Optional[int] = None
    StreetName: Optional[str] = None
    Respond: Optional[str] = None
    Size: Optional[str] = None
    SecurityGameOrAlarm: Optional[bool] = None
    Dog: Optional[str] = None
    Age: Optional[str] = None
    Gender: Optional[str] = None
    Price: Optional[float] = None
