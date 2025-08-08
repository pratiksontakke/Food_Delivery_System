from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from typing import Optional, List
from api.models.menu_item import MenuItem
from api.models.restaurant import Restaurant
from api.schemas.menu_item import MenuItemCreate, MenuItemUpdate

async def create_menu_item(db: AsyncSession, restaurant_id: int, data: MenuItemCreate) -> MenuItem:
    menu_item = MenuItem(**data.model_dump(), restaurant_id=restaurant_id)
    db.add(menu_item)
    await db.commit()
    await db.refresh(menu_item)
    return menu_item

async def get_menu_items(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[MenuItem]:
    result = await db.execute(
        select(MenuItem).offset(skip).limit(limit).order_by(MenuItem.created_at.desc())
    )
    return result.scalars().all()

async def get_menu_item(db: AsyncSession, item_id: int) -> Optional[MenuItem]:
    result = await db.execute(select(MenuItem).where(MenuItem.id == item_id))
    return result.scalar_one_or_none()

async def get_menu_item_with_restaurant(db: AsyncSession, item_id: int) -> Optional[MenuItem]:
    result = await db.execute(
        select(MenuItem).options(selectinload(MenuItem.restaurant)).where(MenuItem.id == item_id)
    )
    return result.scalar_one_or_none()

async def get_restaurant_menu_items(db: AsyncSession, restaurant_id: int) -> List[MenuItem]:
    result = await db.execute(
        select(MenuItem)
        .where(MenuItem.restaurant_id == restaurant_id)
        .order_by(MenuItem.category, MenuItem.name)
    )
    return result.scalars().all()

async def get_restaurant_with_menu(db: AsyncSession, restaurant_id: int) -> Optional[Restaurant]:
    result = await db.execute(
        select(Restaurant)
        .options(selectinload(Restaurant.menu_items))
        .where(Restaurant.id == restaurant_id)
    )
    return result.scalar_one_or_none()

async def update_menu_item(db: AsyncSession, menu_item: MenuItem, data: MenuItemUpdate) -> MenuItem:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(menu_item, field, value)
    await db.commit()
    await db.refresh(menu_item)
    return menu_item

async def delete_menu_item(db: AsyncSession, menu_item: MenuItem):
    await db.delete(menu_item)
    await db.commit()

async def search_menu_items(
    db: AsyncSession, 
    category: Optional[str] = None, 
    vegetarian: Optional[bool] = None,
    vegan: Optional[bool] = None,
    available_only: bool = True,
    skip: int = 0,
    limit: int = 100
) -> List[MenuItem]:
    query = select(MenuItem)
    
    if available_only:
        query = query.where(MenuItem.is_available == True)
    
    if category:
        query = query.where(MenuItem.category == category)
    
    if vegetarian is not None:
        query = query.where(MenuItem.is_vegetarian == vegetarian)
    
    if vegan is not None:
        query = query.where(MenuItem.is_vegan == vegan)
    
    query = query.offset(skip).limit(limit).order_by(MenuItem.name)
    
    result = await db.execute(query)
    return result.scalars().all()

async def get_restaurant_average_price(db: AsyncSession, restaurant_id: int) -> Optional[float]:
    result = await db.execute(
        select(func.avg(MenuItem.price))
        .where(MenuItem.restaurant_id == restaurant_id)
        .where(MenuItem.is_available == True)
    )
    return result.scalar()