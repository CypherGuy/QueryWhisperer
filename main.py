import os
from fastapi import FastAPI
from backend.database import engine
from backend import models as mdls
from backend.routes.auth import router as auth_router
from backend.routes.users import router as users_router
from backend.routes.query import router as query_router
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

mdls.Base.metadata.create_all(bind=engine)


@app.get("/")
async def read_root() -> dict[str, str]:
    return {"message": "Connected to PostgreSQL! If you're looking for the frontend, you can find it at https://querywhisperer.up.railway.app"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000)),
        reload=False
    )
