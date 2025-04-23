import os
from typing import Any, Generator
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
from sqlalchemy.orm.session import Session


from pathlib import Path
load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env.production")
load_dotenv(dotenv_path="backend/.env.production")

postgres_password: str | None = os.getenv("POSTGRES_PASSWORD")

SQLALCHEMY_DATABASE_URL: str = f"postgresql://postgres:{postgres_password}@localhost:5432/querywhisperer_db"


engine: Engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db_session() -> Generator[Session, Any, None]:
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
