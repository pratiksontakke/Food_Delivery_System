from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, func, ForeignKey, Integer
from typing import TYPE_CHECKING
from datetime import datetime
from api.db.database import Base

if TYPE_CHECKING:
    from .customer import Customer
    from .restaurant import Restaurant
    from .order import Order

class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    restaurant_id: Mapped[int] = mapped_column(ForeignKey("restaurants.id"))
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), unique=True)
    rating: Mapped[int] = mapped_column(Integer, nullable=False) # Rating from 1 to 5
    comment: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    customer: Mapped["Customer"] = relationship("Customer", back_populates="reviews")
    restaurant: Mapped["Restaurant"] = relationship("Restaurant", back_populates="reviews")
    order: Mapped["Order"] = relationship("Order", back_populates="review")