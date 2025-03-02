import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

postgres_password = os.getenv("POSTGRES_PASSWORD")
print(postgres_password)

SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:{postgres_password}@localhost:5432/querywhisperer_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():  # Get the database session
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
