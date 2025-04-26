from fastapi import HTTPException
from sqlalchemy.orm import Session
from backend import models, schemas
from passlib.context import CryptContext


pwd_context = CryptContext(
    schemes=["bcrypt"]
)


def create_user(db: Session, user: schemas.UserCreate):
    existing_user = db.query(models.User).filter(
        (models.User.username == user.username) | (
            models.User.email == user.email)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=409, detail="User already exists")

    new_user = models.User(username=user.username,
                           email=user.email, hashed_password=pwd_context.hash(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user(db: Session, user_id: int) -> models.User:
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_all_users(db: Session) -> schemas.List[models.User]:
    return db.query(models.User).all()


def update_user(db: Session, user_id: int, update_data: schemas.UserUpdate) -> models.User:
    user: models.User | None = db.query(models.User).filter(
        models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for attr, value in update_data.model_dump(exclude_unset=True).items():
        setattr(user, attr, value)

    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int) -> models.User:
    user: models.User | None = db.query(models.User).filter(
        models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return user
