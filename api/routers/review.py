from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from api.db.database import get_db
from api.crud import review as crud
from api.crud import order as order_crud
from api.crud import restaurant as restaurant_crud
from api.crud import customer as customer_crud
from api.schemas.review import ReviewCreate, ReviewRead, ReviewWithCustomer, ReviewWithRestaurant
from api.models.order import OrderStatus

router = APIRouter(tags=["Reviews"])

@router.post("/orders/{order_id}/review", response_model=ReviewRead, status_code=201)
async def add_review_for_order(
    order_id: int,
    data: ReviewCreate,
    db: AsyncSession = Depends(get_db)
):
    order = await order_crud.get_order_details(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order.order_status != OrderStatus.delivered:
        raise HTTPException(status_code=400, detail="Review can only be added for delivered orders.")
        
    if order.review:
        raise HTTPException(status_code=400, detail="A review for this order already exists.")

    return await crud.add_review(db, order, data)

@router.get("/restaurants/{restaurant_id}/reviews", response_model=List[ReviewWithCustomer])
async def get_all_restaurant_reviews(restaurant_id: int, db: AsyncSession = Depends(get_db)):
    restaurant = await restaurant_crud.get_restaurant(db, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return await crud.get_restaurant_reviews(db, restaurant_id)

@router.get("/customers/{customer_id}/reviews", response_model=List[ReviewWithRestaurant])
async def get_all_customer_reviews(customer_id: int, db: AsyncSession = Depends(get_db)):
    customer = await customer_crud.get_customer(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return await crud.get_customer_reviews(db, customer_id)