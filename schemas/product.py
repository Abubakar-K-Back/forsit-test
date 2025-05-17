from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field

# Category Tabels
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# product tables
class ProductBase(BaseModel):
    sku: str
    name: str
    description: Optional[str] = None
    price: float = Field(..., ge=0)
    category_id: int
    image_url: Optional[str] = None
    is_active: bool = True

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(None, ge=0)
    category_id: Optional[int] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = None

class Product(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime
    class Config:
        orm_mode = True

class ProductWithInventory(Product):
    inventory_quantity: int
    low_stock_threshold: int
    
    class Config:
        orm_mode = True