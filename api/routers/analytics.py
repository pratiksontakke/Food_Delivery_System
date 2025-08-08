from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from api.db.database import get_db
from api.crud import analytics as crud
from api.crud import restaurant as restaurant_crud
from api.crud import customer as customer_crud
from api.schemas.analytics import RestaurantAnalytics, CustomerAnalytics

router = APIRouter(tags=["Analytics"])

@router.get("/restaurants/{restaurant_id}/analytics", response_model=RestaurantAnalytics)
async def get_restaurant_analytics(restaurant_id: int, db: AsyncSession = Depends(get_db)):
    restaurant = await restaurant_crud.get_restaurant(db, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return await crud.get_restaurant_performance(db, restaurant_id)

@router.get("/customers/{customer_id}/analytics", response_model=CustomerAnalytics)
async def get_customer_analytics_data(customer_id: int, db: AsyncSession = Depends(get_db)):
    customer = await customer_crud.get_customer(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return await crud.get_customer_analytics(db, customer_id)