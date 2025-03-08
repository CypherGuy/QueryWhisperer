from backend.database import Base, engine
from fastapi import FastAPI
from backend.routes import users
from backend.routes.auth import router as auth_router  # Import auth routes

app = FastAPI()

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])

Base.metadata.create_all(bind=engine)


@app.get("/")
async def read_root():
    return {"message": "Connected to PostgreSQL!"}
