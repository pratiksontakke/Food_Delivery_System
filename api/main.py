# /api/main.py

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager

from api.models import restaurant as restaurant_model 
from api.db.database import Base, engine
from api.routers import restaurant as restaurant_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
def home_page():
    return RedirectResponse("/docs")

app.include_router(restaurant_router.router)