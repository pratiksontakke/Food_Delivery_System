from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from decimal import Decimal
from typing import List, Optional

from api.models.order import Order, OrderStatus
from api.models.order_item import OrderItem
from api.models.menu_item import MenuItem
from api.schemas.order import OrderCreate

async def place_order(db: AsyncSession, customer_id: int, data: OrderCreate) -> Order:
    total_amount = Decimal(0)
    order_items_to_create = []

    for item_data in data.items:
        menu_item = await db.get(MenuItem, item_data.menu_item_id)
        if not menu_item or menu_item.restaurant_id != data.restaurant_id:
            raise ValueError(f"Invalid menu item ID: {item_data.menu_item_id}")
        if not menu_item.is_available:
            raise ValueError(f"Menu item '{menu_item.name}' is not available.")
        
        item_price = menu_item.price
        total_amount += item_price * item_data.quantity
        
        order_items_to_create.append(OrderItem(
            menu_item_id=item_data.menu_item_id,
            quantity=item_data.quantity,
            item_price=item_price,
            special_requests=item_data.special_requests
        ))

    new_order = Order(
        customer_id=customer_id,
        restaurant_id=data.restaurant_id,
        total_amount=total_amount,
        delivery_address=data.delivery_address,
        special_instructions=data.special_instructions,
        items=order_items_to_create
    )

    db.add(new_order)
    await db.commit()
    await db.refresh(new_order, attribute_names=['items'])
    return new_order

async def get_order_details(db: AsyncSession, order_id: int) -> Optional[Order]:
    result = await db.execute(
        select(Order)
        .options(
            selectinload(Order.items).selectinload(OrderItem.menu_item),
            selectinload(Order.customer),
            selectinload(Order.restaurant)
        )
        .where(Order.id == order_id)
    )
    return result.scalar_one_or_none()

async def update_order_status(db: AsyncSession, order: Order, status: OrderStatus) -> Order:
    order.order_status = status
    await db.commit()
    await db.refresh(order)
    return order

async def get_customer_orders(db: AsyncSession, customer_id: int) -> List[Order]:
    result = await db.execute(
        select(Order)
        .where(Order.customer_id == customer_id)
        .order_by(Order.order_date.desc())
    )
    return result.scalars().all()

async def get_restaurant_orders(db: AsyncSession, restaurant_id: int) -> List[Order]:
    result = await db.execute(
        select(Order)
        .where(Order.restaurant_id == restaurant_id)
        .order_by(Order.order_date.desc())
    )
    return result.scalars().all()