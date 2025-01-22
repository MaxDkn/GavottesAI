from supabase import create_client, Client
from pydantic import BaseModel
import os
from dotenv import load_dotenv


class InsertHouse(BaseModel):
    street_number: int
    street_name: str
    security_gate: bool


load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)


sql = """
CREATE TABLE IF NOT EXISTS country_characteristic (
    id SERIAL PRIMARY KEY,
    country TEXT,
    daytime TIMESTAMP DEFAULT now(),
    pib INTEGER,
    is_developed BOOLEAN,
    area INTEGER
);
"""

print(supabase.rpc("sql", {"sql": sql}))
