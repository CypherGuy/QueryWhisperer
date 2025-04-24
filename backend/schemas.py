from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional, List


# === User Schemas ===

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
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

# === Auth Schemas ===


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


# === Query + Text-to-SQL Schemas ===

class TableSchema(BaseModel):
    table: str
    columns: List[str]


class QueryRequest(BaseModel):
    question: str
    db_schema: List[TableSchema] = []
    api_key: Optional[str] = None


class QueryResponse(BaseModel):
    generated_sql: str
