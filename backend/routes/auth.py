import datetime
import os
from fastapi import APIRouter, Body, Depends, HTTPException, status
from jose import JWTError
import jwt
from dotenv import load_dotenv
from passlib.context import CryptContext
from pytest import Session
from backend.database import get_db_session
from backend import CRUD, models, schemas
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

load_dotenv()

router = APIRouter()

SECRET_KEY = os.getenv("SECRET_JWT_KEY")
ALGORITHM = "HS256"
# Set the expiration time for the token (minutes), no matter what, the user will be logged out after this time
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7
pwd_context = CryptContext(schemes=["bcrypt"])


def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    expire = datetime.now(timezone.utc) + expires_delta
    data.update({"exp": expire, "user_email": str(data["user_email"])})
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/refresh", response_model=schemas.Token)
async def refresh_access_token(
    # Body() expects JSON like { "refresh_token": "..." }
    refresh_token: str = Body(..., embed=True),
    db: Session = Depends(get_db_session)
):
    # Decode the refresh token
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email = payload.get("user_email")
        if user_email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        user = db.query(models.User).filter(
            models.User.email == user_email).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    new_access_token = create_access_token(
        data={"user_email": str(user.email)},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    new_refresh_token = create_access_token(
        data={"user_email": str(user.email)},
        expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )
    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }


@router.post("/register", response_model=schemas.UserResponse)
async def register_user(user: schemas.UserCreate, db: Session = Depends(get_db_session)):
    return CRUD.create_user(db=db, user=user)


@router.post("/login", response_model=schemas.TokenPair)
async def login_for_access_token(form_data: schemas.UserLogin, db: Session = Depends(get_db_session)):
    user = db.query(models.User).filter(
        models.User.email == form_data.email).first()
    if user is None or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token = create_access_token(
        data={"user_email": str(user.email)},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = create_access_token(
        data={"user_email": str(user.email)},
        expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


# Run checks here for confirming the user
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email = payload.get("user_email")
        if user_email is None:
            raise credentials_exception
        user = db.query(models.User).filter(
            models.User.email == user_email).first()
        if user is None:
            raise credentials_exception
        token_expiry: int = payload.get("exp")
        if token_expiry is None or token_expiry < int(datetime.now(timezone.utc).timestamp()):
            raise "Token has expired. Please log in again."
    except JWTError:
        raise credentials_exception
    return user


@router.get("/users/me", response_model=schemas.UserResponse)
async def read_users_me(current_user: schemas.UserResponse = Depends(get_current_user)):
    return current_user
