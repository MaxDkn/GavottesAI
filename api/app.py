from fastapi import FastAPI
import uvicorn
from dotenv import load_dotenv
import os
from supabase import create_client, Client
from pydantic import BaseModel


class InsertHouse(BaseModel):
    street_number: int
    street_name: str
    security_gate: bool


load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)


app = FastAPI()


@app.post('/create_house')
def create_house_into_db(house: InsertHouse):
    print(house)
    response = (
        supabase.table("house_information")
        .insert(house.dict())
        .execute()
    )
    return response


@app.get("/get_data")
def hello_world():
    response = supabase.table("house_information").select("*").execute()
    return response


if __name__ == '__main__':
    uvicorn.run("app:app")
