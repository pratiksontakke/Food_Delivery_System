from pydantic import BaseModel
from decimal import Decimal
from typing import List, Optional

class PopularItem(BaseModel):
    item_name: str
    quantity_sold: int

class RestaurantAnalytics(BaseModel):
    total_revenue: Decimal
    total_orders: int
    average_rating: float
    popular_items: List[PopularItem]

class CustomerAnalytics(BaseModel):
    total_spending: Decimal
    total_orders: int
    favorite_restaurant: Optional[str] = None