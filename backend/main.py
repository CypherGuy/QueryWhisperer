from fastapi import FastAPI
from .database import engine, Base
from . import models

app = FastAPI()

# 🚀 This creates the tables in PostgreSQL if they don't exist
models.Base.metadata.create_all(bind=engine)


@app.get("/")
async def read_root():
    return {"message": "Connected to PostgreSQL!"}
