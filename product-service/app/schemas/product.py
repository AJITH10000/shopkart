from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

class CategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryResponse(BaseModel):
    id: UUID
    name: str
    description: Optional[str]
    created_at: datetime
    class Config:
        from_attributes = True

class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int = 0
    sku: str
    image_url: Optional[str] = None
    category_id: Optional[UUID] = None

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = None

class ProductResponse(BaseModel):
    id: UUID
    name: str
    description: Optional[str]
    price: float
    stock: int
    sku: str
    image_url: Optional[str]
    is_active: bool
    category_id: Optional[UUID]
    created_at: datetime
    class Config:
        from_attributes = True
