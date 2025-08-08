from datetime import time, datetime
from typing import Optional
from pydantic import BaseModel, Field, constr

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




# Notes: 
# **One-line difference:**

# * **`constr()`** creates a **new custom string type** with built-in validation rules.
# * **`Field()`** applies **validation and metadata to a specific field** without changing its type.

# **When to use:**

# * **Use `constr()`** when you need a **reusable, strongly-typed constrained string** across multiple models.
# * **Use `Field()`** when the **rules are specific to one field** or you also want to add docs/metadata in the same place.

# orm_mode = True allows FastAPI to convert SQLAlchemy objects directly into JSON responses.

