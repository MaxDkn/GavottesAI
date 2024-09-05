import datetime
from typing import Optional
from pydantic import BaseModel


# User models
class UserCreate(BaseModel):
    username: str
    password: str


class User(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


class UserResponse(User):
    pass


# House models
class HouseBase(BaseModel):
    AddressNumber: int
    StreetName: str
    Respond: bool
    Size: str
    SecurityGateOrAlarm: bool
    Dog: str
    Age: Optional[str] = None
    Gender: Optional[str] = None
    Price: float

    class Config:
        extra = "forbid"


class HouseCreate(HouseBase):
    pass


class HouseResponse(HouseBase):
    id: int
    SellerID: int
    DayTime: datetime.datetime

    class Config:
        from_attributes = True


class GetHouseID(BaseModel):
    id: int

    class Config:
        from_attributes = True
        extra = 'forbid'


class EditHouse(GetHouseID):
    AddressNumber: Optional[int] = None
    StreetName: Optional[str] = None
    Respond: Optional[bool] = None
    Size: Optional[str] = None
    SecurityGateOrAlarm: Optional[bool] = None
    Dog: Optional[str] = None
    Age: Optional[str] = None
    Gender: Optional[str] = None
    Price: Optional[float] = None
