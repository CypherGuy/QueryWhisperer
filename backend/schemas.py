from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    username: str
    email: str
    password: str

    class Config:  # Ensures FastAPI returns db objects as JSON responses post-update
        orm_mode = True


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool

    class Config:
        orm_mode = True
