from fastapi import FastAPI
from .database import engine
from . import models
from backend.routes.auth import router as auth_router
from backend.routes.users import router as users_router

app = FastAPI()
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(users_router, prefix="/users", tags=["Users"])

models.Base.metadata.create_all(bind=engine)


@app.get("/")
async def read_root():
    return {"message": "Connected to PostgreSQL!"}
