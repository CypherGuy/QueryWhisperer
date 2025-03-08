import datetime
import os
from fastapi import APIRouter, Depends, HTTPException, status
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
# Set the expiration time for the token (minutes)
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"])


def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    expire = datetime.now(timezone.utc) + expires_delta
    data.update({"exp": expire, "sub": str(data["sub"])})
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/register", response_model=schemas.UserResponse)
async def register_user(user: schemas.UserCreate, db: Session = Depends(get_db_session)):
    return CRUD.create_user(db=db, user=user)


@router.post("/login")
async def login_for_access_token(form_data: schemas.UserLogin, db: Session = Depends(get_db_session)):
    user = db.query(models.User).filter(
        models.User.email == form_data.email).first()

    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": str(user.email)})
    return {"access_token": access_token, "token_type": "bearer"}


# Run checks here for confirming the user
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        subject = payload.get("sub")
        if subject is None:
            raise credentials_exception
        user = db.query(models.User).filter(
            models.User.email == subject).first()
        if user is None:
            raise credentials_exception
        token_expiry: int = payload.get("exp")
        if token_expiry is None or token_expiry < int(datetime.now(timezone.utc).timestamp()):
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return user


@router.get("/users/me", response_model=schemas.UserResponse)
async def read_users_me(current_user: schemas.UserResponse = Depends(get_current_user)):
    return current_user
