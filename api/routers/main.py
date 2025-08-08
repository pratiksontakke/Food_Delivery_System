from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager

# Import all models to ensure they are registered with Base
from api.models import customer, restaurant, menu_item, order, order_item, review
from api.db.database import Base, engine

# Import all routers
from api.routers import (
    restaurant as restaurant_router,
    menu_item as menu_item_router,
    customer as customer_router,
    order as order_router,
    review as review_router,
    analytics as analytics_router
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title="Complete Food Delivery System API",
    description="A comprehensive API for a food delivery ecosystem.",
    version="3.0.0",
    lifespan=lifespan
)

@app.get("/")
def home_page():
    return RedirectResponse("/docs")

# Include all routers
app.include_router(restaurant_router.router)
app.include_router(menu_item_router.router)
app.include_router(customer_router.router)
app.include_router(order_router.router)
app.include_router(review_router.router)
app.include_router(analytics_router.router)