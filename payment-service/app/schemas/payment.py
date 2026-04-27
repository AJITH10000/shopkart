from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional
from app.models.payment import PaymentStatus, PaymentMethod

class PaymentCreate(BaseModel):
    order_id: UUID
    user_id: UUID
    amount: float
    currency: str = "INR"
    method: PaymentMethod

class PaymentResponse(BaseModel):
    id: UUID
    order_id: UUID
    user_id: UUID
    amount: float
    currency: str
    method: PaymentMethod
    status: PaymentStatus
    transaction_id: Optional[str]
    failure_reason: Optional[str]
    created_at: datetime
    class Config:
        from_attributes = True
