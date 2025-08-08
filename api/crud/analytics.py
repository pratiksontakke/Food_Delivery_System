from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from sqlalchemy.orm import selectinload
from decimal import Decimal
from typing import Dict, Any

from api.models import Customer, Restaurant, Order, OrderItem, MenuItem

async def get_restaurant_performance(db: AsyncSession, restaurant_id: int) -> Dict[str, Any]:
    # Total Revenue
    revenue_result = await db.execute(
        select(func.sum(Order.total_amount))
        .where(Order.restaurant_id == restaurant_id)
        .where(Order.order_status == 'delivered')
    )
    total_revenue = revenue_result.scalar_one_or_none() or Decimal('0.0')

    # Total Orders
    orders_count_result = await db.execute(
        select(func.count(Order.id))
        .where(Order.restaurant_id == restaurant_id)
    )
    total_orders = orders_count_result.scalar_one()

    # Popular Menu Items (Top 5)
    popular_items_result = await db.execute(
        select(MenuItem.name, func.sum(OrderItem.quantity).label('total_quantity'))
        .join(OrderItem, MenuItem.id == OrderItem.menu_item_id)
        .join(Order, OrderItem.order_id == Order.id)
        .where(Order.restaurant_id == restaurant_id)
        .group_by(MenuItem.name)
        .order_by(desc('total_quantity'))
        .limit(5)
    )
    popular_items = [{"item_name": name, "quantity_sold": qty} for name, qty in popular_items_result.all()]

    return {
        "total_revenue": total_revenue,
        "total_orders": total_orders,
        "average_rating": (await db.get(Restaurant, restaurant_id)).rating,
        "popular_items": popular_items
    }

async def get_customer_analytics(db: AsyncSession, customer_id: int) -> Dict[str, Any]:
    # Total Spending
    spending_result = await db.execute(
        select(func.sum(Order.total_amount))
        .where(Order.customer_id == customer_id)
        .where(Order.order_status == 'delivered')
    )
    total_spending = spending_result.scalar_one_or_none() or Decimal('0.0')

    # Total Orders
    orders_count_result = await db.execute(
        select(func.count(Order.id))
        .where(Order.customer_id == customer_id)
    )
    total_orders = orders_count_result.scalar_one()

    # Favorite Restaurant (by order count)
    fav_restaurant_result = await db.execute(
        select(Restaurant.name, func.count(Order.id).label('order_count'))
        .join(Order, Restaurant.id == Order.restaurant_id)
        .where(Order.customer_id == customer_id)
        .group_by(Restaurant.name)
        .order_by(desc('order_count'))
        .limit(1)
    )
    favorite_restaurant = fav_restaurant_result.first()

    return {
        "total_spending": total_spending,
        "total_orders": total_orders,
        "favorite_restaurant": favorite_restaurant.name if favorite_restaurant else None
    }