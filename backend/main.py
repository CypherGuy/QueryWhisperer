from fastapi import FastAPI
from .database import engine
from . import models
from backend.routes.auth import router as auth_router
from backend.routes.users import router as users_router
from backend.routes.query import router as query_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(query_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)


@app.get("/")
async def read_root() -> dict[str, str]:
    return {"message": "Connected to PostgreSQL!"}
