from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from api.crud.menu_item import (
    create_menu_item, 
    get_menu_items, 
    get_menu_item, 
    get_menu_item_with_restaurant,
    update_menu_item, 
    delete_menu_item,
    search_menu_items
)
from api.crud.restaurant import get_restaurant
from api.db.database import get_db
from api.schemas.menu_item import MenuItemCreate, MenuItemRead, MenuItemUpdate, MenuItemWithRestaurant

router = APIRouter(prefix="/menu-items", tags=["Menu Items"])

@router.post("/", response_model=MenuItemRead, 
             summary="Create menu item for a specific restaurant")
async def create_item(
    restaurant_id: int = Query(..., description="Restaurant ID to add menu item to"),
    data: MenuItemCreate = ...,
    db: AsyncSession = Depends(get_db)
):
    # Check if restaurant exists
    restaurant = await get_restaurant(db, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    return await create_menu_item(db, restaurant_id, data)

@router.get("/", response_model=List[MenuItemRead])
async def list_all_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db)
):
    return await get_menu_items(db, skip=skip, limit=limit)

@router.get("/search", response_model=List[MenuItemRead])
async def search_items(
    category: Optional[str] = Query(None, description="Filter by category"),
    vegetarian: Optional[bool] = Query(None, description="Filter vegetarian items"),
    vegan: Optional[bool] = Query(None, description="Filter vegan items"),
    available_only: bool = Query(True, description="Show only available items"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db)
):
    return await search_menu_items(
        db, 
        category=category, 
        vegetarian=vegetarian, 
        vegan=vegan,
        available_only=available_only,
        skip=skip, 
        limit=limit
    )

@router.get("/{item_id}", response_model=MenuItemRead)
async def get_item(item_id: int, db: AsyncSession = Depends(get_db)):
    menu_item = await get_menu_item(db, item_id)
    if not menu_item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return menu_item

@router.get("/{item_id}/with-restaurant", response_model=MenuItemWithRestaurant)
async def get_item_with_restaurant(item_id: int, db: AsyncSession = Depends(get_db)):
    menu_item = await get_menu_item_with_restaurant(db, item_id)
    if not menu_item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return menu_item

@router.put("/{item_id}", response_model=MenuItemRead)
async def update_item(
    item_id: int, 
    data: MenuItemUpdate, 
    db: AsyncSession = Depends(get_db)
):
    menu_item = await get_menu_item(db, item_id)
    if not menu_item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return await update_menu_item(db, menu_item, data)

@router.delete("/{item_id}")
async def delete_item(item_id: int, db: AsyncSession = Depends(get_db)):
    menu_item = await get_menu_item(db, item_id)
    if not menu_item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    await delete_menu_item(db, menu_item)
    return {"detail": "Menu item deleted successfully"}