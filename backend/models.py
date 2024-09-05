from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, func


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)


class House(Base):
    __tablename__ = "house_informations"

    id = Column(Integer, primary_key=True, index=True)
    SellerID = Column(Integer)
    AddressNumber = Column(Integer)
    StreetName = Column(String)
    DayTime = Column(DateTime, default=func.now())
    Respond = Column(Boolean)
    Size = Column(String)
    SecurityGateOrAlarm = Column(Boolean)
    Dog = Column(String)
    Age = Column(String, nullable=True)
    Gender = Column(String, nullable=True)
    Price = Column(Float)
