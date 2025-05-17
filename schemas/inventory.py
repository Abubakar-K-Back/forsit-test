from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field

class InventoryBase(BaseModel):
    product_id: int
    quantity: int = Field(..., ge=0)
    low_stock_threshold: int = Field(..., ge=0)

class InventoryCreate(InventoryBase):
    pass

class InventoryUpdate(BaseModel):
    quantity: int = Field(..., ge=0)
    low_stock_threshold: Optional[int] = Field(None, ge=0)
    note: Optional[str] = None

class Inventory(InventoryBase):
    id: int
    last_restock_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    class Config:
        orm_mode = True

class LowStockProduct(BaseModel):
    product_id: int
    sku: str
    name: str
    current_quantity: int
    low_stock_threshold: int
    class Config:
        orm_mode = True

class InventoryTransactionBase(BaseModel):
    product_id: int
    quantity_change: int
    transaction_type: str
    reference_id: Optional[str] = None
    note: Optional[str] = None

class InventoryTransaction(InventoryTransactionBase):
    id: int
    created_at: datetime
  
    class Config:
        orm_mode = True