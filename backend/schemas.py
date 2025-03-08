from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    username: str
    email: str
    password: str

    # Ensures FastAPI returns db objects as JSON responses post-update
    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    email: str
    password: str

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
