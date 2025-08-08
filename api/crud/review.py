from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from api.models.review import Review
from api.models.restaurant import Restaurant
from api.models.order import Order
from api.schemas.review import ReviewCreate
from typing import List

async def add_review(db: AsyncSession, order: Order, data: ReviewCreate) -> Review:
    review = Review(
        customer_id=order.customer_id,
        restaurant_id=order.restaurant_id,
        order_id=order.id,
        rating=data.rating,
        comment=data.comment
    )
    db.add(review)
    
    # Update restaurant's average rating
    restaurant = await db.get(Restaurant, order.restaurant_id)
    if restaurant:
        # Get all ratings for the restaurant
        result = await db.execute(
            select(func.avg(Review.rating)).where(Review.restaurant_id == order.restaurant_id)
        )
        avg_rating = result.scalar()
        restaurant.rating = round(avg_rating, 2) if avg_rating else 0.0

    await db.commit()
    await db.refresh(review)
    return review

async def get_restaurant_reviews(db: AsyncSession, restaurant_id: int) -> List[Review]:
    result = await db.execute(
        select(Review)
        .options(selectinload(Review.customer))
        .where(Review.restaurant_id == restaurant_id)
        .order_by(Review.created_at.desc())
    )
    return result.scalars().all()

async def get_customer_reviews(db: AsyncSession, customer_id: int) -> List[Review]:
    result = await db.execute(
        select(Review)
        .options(selectinload(Review.restaurant))
        .where(Review.customer_id == customer_id)
        .order_by(Review.created_at.desc())
    )
    return result.scalars().all()