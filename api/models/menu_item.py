from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Float, Boolean, Integer, DateTime, func, ForeignKey, DECIMAL
from typing import Optional, TYPE_CHECKING, List
from datetime import datetime
from decimal import Decimal
from api.db.database import Base

if TYPE_CHECKING:
    from .restaurant import Restaurant
    from .order_item import OrderItem

class MenuItem(Base):
    __tablename__ = "menu_items"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    price: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    is_vegetarian: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_vegan: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_available: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    preparation_time: Mapped[int] = mapped_column(Integer, nullable=False)  # in minutes
    restaurant_id: Mapped[int] = mapped_column(ForeignKey("restaurants.id", ondelete="CASCADE"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    
    # Relationships
    restaurant: Mapped["Restaurant"] = relationship("Restaurant", back_populates="menu_items")
    order_items: Mapped[List["OrderItem"]] = relationship("OrderItem", back_populates="menu_item")