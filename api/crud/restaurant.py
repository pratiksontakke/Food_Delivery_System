from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from api.models.restaurant import Restaurant
from api.schemas.restaurant import RestaurantCreate, RestaurantUpdate

async def create_restaurant(db: AsyncSession, data: RestaurantCreate) -> Restaurant:
    restaurant = Restaurant(**data.model_dump())
    db.add(restaurant)
    await db.commit()
    await db.refresh(restaurant)
    return restaurant

async def get_restaurants(db: AsyncSession):
    result = await db.execute(select(Restaurant))
    return result.scalars().all()

async def get_restaurant(db: AsyncSession, restaurant_id: int):
    result = await db.execute(select(Restaurant).where(Restaurant.id == restaurant_id))
    return result.scalar_one_or_none()

async def update_restaurant(db: AsyncSession, restaurant: Restaurant, data: RestaurantUpdate):
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(restaurant, field, value)
    await db.commit()
    await db.refresh(restaurant)
    return restaurant

async def delete_restaurant(db: AsyncSession, restaurant: Restaurant):
    await db.delete(restaurant)
    await db.commit()
