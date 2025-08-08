from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, DECIMAL, Integer, String
from typing import Optional, TYPE_CHECKING
from decimal import Decimal
from api.db.database import Base

if TYPE_CHECKING:
    from .order import Order
    from .menu_item import MenuItem

class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"))
    menu_item_id: Mapped[int] = mapped_column(ForeignKey("menu_items.id"))
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    item_price: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    special_requests: Mapped[Optional[str]] = mapped_column(String(255))

    # Relationships
    order: Mapped["Order"] = relationship("Order", back_populates="items")
    menu_item: Mapped["MenuItem"] = relationship("MenuItem", back_populates="order_items")