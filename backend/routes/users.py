from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend import CRUD, models, schemas
from backend.routes.auth import get_current_user
from backend.database import get_db_session

router = APIRouter()


@router.post("/", response_model=schemas.UserResponse)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db_session)):
    return CRUD.create_user(db=db, user=user)


@router.get("/{user_id}", response_model=schemas.UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db_session)):
    return CRUD.get_user(db=db, user_id=user_id)


@router.get("/", response_model=list[schemas.UserResponse])
async def get_all_users(db: Session = Depends(get_db_session)):
    return CRUD.get_all_users(db=db)


@router.put("/{user_id}", response_model=schemas.UserResponse)
async def update_user(
    user_id: int,
    user_update_schema: schemas.UserUpdate,
    db: Session = Depends(get_db_session),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return CRUD.update_user(db=db, user_id=user_id, update_data=user_update_schema)


@router.delete("/{user_id}", response_model=schemas.UserResponse)
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db_session),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return CRUD.delete_user(db=db, user_id=user_id)
