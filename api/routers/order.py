from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from api.db.database import get_db
from api.crud import order as crud
from api.crud import customer as customer_crud
from api.crud import restaurant as restaurant_crud
from api.schemas.order import OrderCreate, OrderRead, OrderDetails, OrderUpdateStatus
from api.models.order import OrderStatus

router = APIRouter(tags=["Orders"])

@router.post("/customers/{customer_id}/orders/", response_model=OrderRead, status_code=201)
async def place_new_order(
    customer_id: int,
    data: OrderCreate,
    db: AsyncSession = Depends(get_db)
):
    # Validate customer and restaurant exist
    customer = await customer_crud.get_customer(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    restaurant = await restaurant_crud.get_restaurant(db, data.restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    try:
        return await crud.place_order(db, customer_id, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/orders/{order_id}", response_model=OrderDetails)
async def get_order_with_details(order_id: int, db: AsyncSession = Depends(get_db)):
    order = await crud.get_order_details(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.put("/orders/{order_id}/status", response_model=OrderRead)
async def update_order_status(
    order_id: int, 
    data: OrderUpdateStatus, 
    db: AsyncSession = Depends(get_db)
):
    order = await crud.get_order_details(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return await crud.update_order_status(db, order, data.status)

@router.get("/customers/{customer_id}/orders", response_model=List[OrderRead])
async def get_customer_order_history(customer_id: int, db: AsyncSession = Depends(get_db)):
    customer = await customer_crud.get_customer(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return await crud.get_customer_orders(db, customer_id)

@router.get("/restaurants/{restaurant_id}/orders", response_model=List[OrderRead])
async def get_restaurant_orders(restaurant_id: int, db: AsyncSession = Depends(get_db)):
    restaurant = await restaurant_crud.get_restaurant(db, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return await crud.get_restaurant_orders(db, restaurant_id)