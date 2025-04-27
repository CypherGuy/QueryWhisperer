from fastapi import FastAPI
from database import engine
import models as models
from routes.auth import router as auth_router
from routes.users import router as users_router
from routes.query import router as query_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://querywhisperer.up.railway.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(query_router)

models.Base.metadata.create_all(bind=engine)


@app.get("/")
async def read_root() -> dict[str, str]:
    return {"message": "Connected to PostgreSQL! If you're looking for the frontend, you can find it at https://querywhisperer.up.railway.app"}
