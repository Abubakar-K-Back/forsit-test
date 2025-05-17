from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)
    unit_price: float = Field(..., ge=0)

class OrderItemCreate(OrderItemBase):
    pass

class OrderItem(OrderItemBase):
    id: int
    subtotal: float
    created_at: datetime
    
    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    order_date: datetime
    status: str
    payment_status: str
    subtotal: float = Field(..., ge=0)
    tax: float = Field(..., ge=0)
    shipping_cost: float = Field(..., ge=0)
    discount: float = Field(0.0, ge=0)
    total: float = Field(..., ge=0)
    marketplace: str

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]

class Order(OrderBase):
    id: int
    order_number: str
    items: List[OrderItem]
    created_at: datetime
    updated_at: datetime
    class Config:
        orm_mode = True