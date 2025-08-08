from datetime import datetime
from typing import Optional, ForwardRef
from pydantic import BaseModel, Field, field_validator
from decimal import Decimal

# Forward reference to avoid circular imports
RestaurantRead = ForwardRef('RestaurantRead')

class MenuItemBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = None
    price: Decimal = Field(..., gt=0, decimal_places=2)
    category: str = Field(..., description="E.g., 'Appetizer', 'Main Course', 'Dessert', 'Beverage'")
    is_vegetarian: bool = Field(default=False)
    is_vegan: bool = Field(default=False)
    is_available: bool = Field(default=True)
    preparation_time: int = Field(..., gt=0, description="Preparation time in minutes")
    
    @field_validator('price')
    @classmethod
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError('Price must be positive')
        return round(v, 2)
    
    @field_validator('category')
    @classmethod
    def validate_category(cls, v):
        allowed_categories = ['Appetizer', 'Main Course', 'Dessert', 'Beverage', 'Snack', 'Side Dish']
        if v not in allowed_categories:
            raise ValueError(f'Category must be one of: {", ".join(allowed_categories)}')
        return v

class MenuItemCreate(MenuItemBase):
    pass

class MenuItemUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = None
    price: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    category: Optional[str] = None
    is_vegetarian: Optional[bool] = None
    is_vegan: Optional[bool] = None
    is_available: Optional[bool] = None
    preparation_time: Optional[int] = Field(None, gt=0)
    
    @field_validator('price')
    @classmethod
    def validate_price(cls, v):
        if v is not None and v <= 0:
            raise ValueError('Price must be positive')
        return v

class MenuItemRead(MenuItemBase):
    id: int
    restaurant_id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = {
        "from_attributes": True
    }

class MenuItemWithRestaurant(MenuItemRead):
    restaurant: 'RestaurantRead'

# Import after class definitions to resolve forward references
from api.schemas.restaurant import RestaurantRead
MenuItemWithRestaurant.model_rebuild()