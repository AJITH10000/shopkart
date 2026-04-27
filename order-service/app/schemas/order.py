from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import List, Optional, Dict, Any
from app.models.order import OrderStatus

class OrderItemCreate(BaseModel):
    product_id: UUID
    product_name: str
    price: float
    quantity: int

class OrderCreate(BaseModel):
    user_id: UUID
    items: List[OrderItemCreate]
    shipping_address: Dict[str, Any]
    notes: Optional[str] = None

class OrderItemResponse(BaseModel):
    id: UUID
    product_id: UUID
    product_name: str
    price: float
    quantity: int
    class Config:
        from_attributes = True

class OrderResponse(BaseModel):
    id: UUID
    user_id: UUID
    status: OrderStatus
    total_amount: float
    shipping_address: Dict[str, Any]
    payment_id: Optional[str]
    notes: Optional[str]
    items: List[OrderItemResponse]
    created_at: datetime
    class Config:
        from_attributes = True

class OrderStatusUpdate(BaseModel):
    status: OrderStatus
    payment_id: Optional[str] = None
