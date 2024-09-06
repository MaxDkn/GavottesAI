import pandas as pd
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter
from sklearn.linear_model import LogisticRegression

from backend.models import House
from backend.database import get_db


ai_router = APIRouter()
global clf 


def load_data(db: Session, /):
    houses = db.query(House).all()
    houses_dict_list = [house.__dict__ for house in houses]

    for house_dict in houses_dict_list:
        house_dict.pop('_sa_instance_state', None)
    return houses_dict_list


def data_processing(data: list[dict]) -> tuple:
    df = pd.DataFrame(data)
    df = df.drop(['AddressNumber', 'StreetName', 'Respond', 'Age', 'Gender', 'id', 'SellerID'], axis=1)

    df['Size'] = df['Size'].map({'Small': 0, 'Medium': 1, 'Big': 2})
    df['SecurityGateOrAlarm'] = df['SecurityGateOrAlarm'].map({False: 0, True: 1})
    df['Dog'] = df['Dog'].map({'No': 0, 'Unknown': 0, 'Small': 1, 'Large': 2})
    df['DayTime'] = pd.to_datetime(df['DayTime']).dt.hour + pd.to_datetime(df['DayTime']).dt.minute / 60
    df['Price'] = df['Price'].map(lambda x: 1 if int(x) > 0 else 0)

    return df[["Size","SecurityGateOrAlarm","Dog","DayTime"]], df["Price"]


@ai_router.get('/coef')
async def ai(db: Session = Depends(get_db)):
    clf = LogisticRegression(random_state=0).fit(*data_processing(load_data(db)))
    return str(clf.coef_)

