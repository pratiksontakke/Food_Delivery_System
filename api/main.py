from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager

from api.models import restaurant as restaurant_model
from api.models import menu_item as menu_item_model
from api.db.database import Base, engine
from api.routers import restaurant as restaurant_router
from api.routers import menu_item as menu_item_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title="Restaurant Menu System API",
    description="A comprehensive API for managing restaurants and their menu items",
    version="2.0.0",
    lifespan=lifespan
)

@app.get("/")
def home_page():
    return RedirectResponse("/docs")

# Include routers
app.include_router(restaurant_router.router)
app.include_router(menu_item_router.router)