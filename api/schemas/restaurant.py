from datetime import time, datetime
from typing import Optional, List, ForwardRef
from pydantic import BaseModel, Field, constr
from decimal import Decimal

# Forward reference to avoid circular imports
MenuItemRead = ForwardRef('MenuItemRead')

class RestaurantBase(BaseModel):
    name: constr(min_length=3, max_length=100)
    description: Optional[str] = None
    cuisine_type: str = Field(..., description="E.g., 'Italian', 'Chinese', 'Indian'")
    address: str
    phone_number: str = Field(..., description="Phone number in format +918888654318")
    rating: float = Field(0.0, ge=0.0, le=5.0)
    is_active: bool = True
    opening_time: time
    closing_time: time

class RestaurantCreate(RestaurantBase):
    pass

class RestaurantUpdate(BaseModel):
    name: Optional[constr(min_length=3, max_length=100)] = None
    description: Optional[str] = None
    cuisine_type: Optional[str] = None
    address: Optional[str] = None
    phone_number: Optional[str] = None
    rating: Optional[float] = Field(None, ge=0.0, le=5.0)
    is_active: Optional[bool] = None
    opening_time: Optional[time] = None
    closing_time: Optional[time] = None

class RestaurantRead(RestaurantBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = {
        "from_attributes": True
    }

class RestaurantWithMenu(RestaurantRead):
    menu_items: List['MenuItemRead'] = []
    average_price: Optional[Decimal] = None

# Import after class definitions to resolve forward references
from api.schemas.menu_item import MenuItemRead
RestaurantWithMenu.model_rebuild()