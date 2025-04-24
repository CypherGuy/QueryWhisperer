import os
from typing import Generator
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
from sqlalchemy.orm.session import Session


from pathlib import Path
load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env.production")

DATABASE_URL: str | None = os.getenv("DATABASE_URL")

engine: Engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db_session() -> Generator[Session, None]:
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
