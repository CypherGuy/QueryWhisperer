from fastapi import Depends, FastAPI
from backend import CRUD, schemas
from sqlalchemy.orm import Session
from .database import engine, get_db_session
from . import models
from backend.routes.auth import router as auth_router

app = FastAPI()
app.include_router(auth_router, prefix="/auth", tags=["Auth"])

models.Base.metadata.create_all(bind=engine)


@app.get("/")
async def read_root():
    return {"message": "Connected to PostgreSQL!"}


@app.post("/users/", response_model=schemas.UserResponse)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db_session)):
    return CRUD.create_user(db=db, user=user)


@app.get("/users/{user_id}", response_model=schemas.UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db_session)):
    return CRUD.get_user(db=db, user_id=user_id)
