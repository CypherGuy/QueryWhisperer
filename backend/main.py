from fastapi import Depends, FastAPI
from backend import CRUD, schemas
from sqlalchemy.orm import Session
from .database import engine, get_db
from . import models

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


@app.get("/")
async def read_root():
    return {"message": "Connected to PostgreSQL!"}


@app.post("/users/")
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return CRUD.create_user(db=db, user=user)


@app.get("/users/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    return CRUD.get_user(db=db, user_id=user_id)
