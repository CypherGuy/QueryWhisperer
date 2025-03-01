from dotenv import load_dotenv
from sqlalchemy import create_engine
import os

load_dotenv()

postgres_password = os.getenv("POSTGRES_PASSWORD")
print(postgres_password)

SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:{postgres_password}@localhost:5432/querywhisperer_db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

try:
    with engine.connect() as conn:
        print("Connected to PostgreSQL!")
except Exception as e:
    print(f"Failed: {e}")
