from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from api.models.restaurant import Restaurant
from api.models.menu_item import MenuItem
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

async def get_restaurant_with_menu(db: AsyncSession, restaurant_id: int):
    result = await db.execute(
        select(Restaurant)
        .options(selectinload(Restaurant.menu_items))
        .where(Restaurant.id == restaurant_id)
    )
    restaurant = result.scalar_one_or_none()
    
    if restaurant:
        # Calculate average price
        avg_price_result = await db.execute(
            select(func.avg(MenuItem.price))
            .where(MenuItem.restaurant_id == restaurant_id)
            .where(MenuItem.is_available == True)
        )
        avg_price = avg_price_result.scalar()
        # Add average price as an attribute for the response
        restaurant.average_price = round(avg_price, 2) if avg_price else None
    
    return restaurant

async def update_restaurant(db: AsyncSession, restaurant: Restaurant, data: RestaurantUpdate):
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(restaurant, field, value)
    await db.commit()
    await db.refresh(restaurant)
    return restaurant

async def delete_restaurant(db: AsyncSession, restaurant: Restaurant):
    await db.delete(restaurant)
    await db.commit()