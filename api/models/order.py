import enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, func, ForeignKey, DECIMAL, Enum
from typing import List, Optional, TYPE_CHECKING
from datetime import datetime
from decimal import Decimal
from api.db.database import Base

if TYPE_CHECKING:
    from .customer import Customer
    from .restaurant import Restaurant
    from .order_item import OrderItem
    from .review import Review

class OrderStatus(enum.Enum):
    placed = "placed"
    confirmed = "confirmed"
    preparing = "preparing"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"
    cancelled = "cancelled"

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    restaurant_id: Mapped[int] = mapped_column(ForeignKey("restaurants.id"))
    order_status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus), default=OrderStatus.placed)
    total_amount: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    delivery_address: Mapped[str] = mapped_column(String(255))
    special_instructions: Mapped[Optional[str]] = mapped_column(String(500))
    order_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    delivery_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    # Relationships
    customer: Mapped["Customer"] = relationship("Customer", back_populates="orders")
    restaurant: Mapped["Restaurant"] = relationship("Restaurant", back_populates="orders")
    items: Mapped[List["OrderItem"]] = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    review: Mapped[Optional["Review"]] = relationship("Review", back_populates="order", uselist=False)