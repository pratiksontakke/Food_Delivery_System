from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from api.crud.restaurant import (
    create_restaurant, 
    delete_restaurant, 
    get_restaurant, 
    get_restaurants, 
    update_restaurant,
    get_restaurant_with_menu
)
from api.crud.menu_item import (
    create_menu_item,
    get_restaurant_menu_items
)
from api.db.database import get_db
from api.schemas.restaurant import RestaurantCreate, RestaurantRead, RestaurantUpdate, RestaurantWithMenu
from api.schemas.menu_item import MenuItemCreate, MenuItemRead
from api.models.restaurant import Restaurant

router = APIRouter(prefix="/restaurants", tags=["Restaurants"])

@router.post("/", response_model=RestaurantRead)
async def create(data: RestaurantCreate, db: AsyncSession = Depends(get_db)):
    return await create_restaurant(db, data)

@router.get("/", response_model=List[RestaurantRead])
async def list_all(db: AsyncSession = Depends(get_db)):
    return await get_restaurants(db)

@router.get("/{restaurant_id}", response_model=RestaurantRead)
async def get(restaurant_id: int, db: AsyncSession = Depends(get_db)):
    restaurant = await get_restaurant(db, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant

@router.get("/{restaurant_id}/with-menu", response_model=RestaurantWithMenu)
async def get_with_menu(restaurant_id: int, db: AsyncSession = Depends(get_db)):
    restaurant = await get_restaurant_with_menu(db, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant

@router.get("/{restaurant_id}/menu", response_model=List[MenuItemRead])
async def get_menu(restaurant_id: int, db: AsyncSession = Depends(get_db)):
    # Check if restaurant exists
    restaurant = await get_restaurant(db, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    return await get_restaurant_menu_items(db, restaurant_id)

@router.post("/{restaurant_id}/menu-items/", response_model=MenuItemRead)
async def add_menu_item(
    restaurant_id: int, 
    data: MenuItemCreate, 
    db: AsyncSession = Depends(get_db)
):
    # Check if restaurant exists
    restaurant = await get_restaurant(db, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    return await create_menu_item(db, restaurant_id, data)

@router.put("/{restaurant_id}", response_model=RestaurantRead)
async def update(restaurant_id: int, data: RestaurantUpdate, db: AsyncSession = Depends(get_db)):
    restaurant = await get_restaurant(db, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return await update_restaurant(db, restaurant, data)

@router.delete("/{restaurant_id}")
async def delete(restaurant_id: int, db: AsyncSession = Depends(get_db)):
    restaurant = await get_restaurant(db, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    await delete_restaurant(db, restaurant)
    return {"detail": "Restaurant deleted successfully"}