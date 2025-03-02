from backend.database import Base, engine
from fastapi import FastAPI
from backend.routes import users

app = FastAPI()
app.include_router(users.router, prefix="/users", tags=["Users"])
Base.metadata.create_all(bind=engine)


@app.get("/")
async def read_root():
    return {"message": "Connected to PostgreSQL!"}
