from pydantic import BaseModel, Field
from datetime import datetime
from decimal import Decimal
from typing import List, Optional, ForwardRef

from api.models.order import OrderStatus

# Forward references for nested schemas
CustomerRead = ForwardRef('CustomerRead')
RestaurantRead = ForwardRef('RestaurantRead')
MenuItemRead = ForwardRef('MenuItemRead')

class OrderItemBase(BaseModel):
    menu_item_id: int
    quantity: int = Field(..., gt=0)
    special_requests: Optional[str] = None

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemRead(OrderItemBase):
    id: int
    item_price: Decimal
    menu_item: MenuItemRead

    model_config = {
        "from_attributes": True
    }

class OrderBase(BaseModel):
    restaurant_id: int
    delivery_address: str
    special_instructions: Optional[str] = None

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]

class OrderUpdateStatus(BaseModel):
    status: OrderStatus

class OrderRead(OrderBase):
    id: int
    customer_id: int
    order_status: OrderStatus
    total_amount: Decimal
    order_date: datetime
    delivery_time: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }

class OrderDetails(OrderRead):
    customer: CustomerRead
    restaurant: RestaurantRead
    items: List[OrderItemRead]

# Resolve forward references
from .customer import CustomerRead
from .restaurant import RestaurantRead
from .menu_item import MenuItemRead

OrderDetails.model_rebuild()
OrderItemRead.model_rebuild()