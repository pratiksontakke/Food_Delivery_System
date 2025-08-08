from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, ForwardRef

CustomerRead = ForwardRef('CustomerRead')
RestaurantRead = ForwardRef('RestaurantRead')

class ReviewBase(BaseModel):
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 to 5")
    comment: Optional[str] = None

class ReviewCreate(ReviewBase):
    pass

class ReviewRead(ReviewBase):
    id: int
    customer_id: int
    restaurant_id: int
    order_id: int
    created_at: datetime
    
    model_config = {
        "from_attributes": True
    }

class ReviewWithCustomer(ReviewRead):
    customer: CustomerRead

class ReviewWithRestaurant(ReviewRead):
    restaurant: RestaurantRead

from .customer import CustomerRead
from .restaurant import RestaurantRead

ReviewWithCustomer.model_rebuild()
ReviewWithRestaurant.model_rebuild()