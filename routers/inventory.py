from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import get_db
from schemas.inventory import (
    Inventory, InventoryUpdate, LowStockProduct, InventoryTransaction
)
from services import inventory_service

router = APIRouter(prefix="/api/inventory", tags=["inventory"])

@router.get("/", response_model=List[Inventory])
def get_inventory_items(skip: int = 0,limit: int = 100,db: Session = Depends(get_db)):
    return inventory_service.get_all_inventory(db, skip, limit)

@router.get("/low-stock", response_model=List[LowStockProduct])
def get_low_stock_products(db: Session = Depends(get_db)):
    return inventory_service.get_low_stock_products(db)

@router.put("/{product_id}", response_model=Inventory)
def update_inventory(product_id: int,inventory_update: InventoryUpdate,db: Session = Depends(get_db)):
    try:
        return inventory_service.update_inventory(db, product_id, inventory_update.quantity, inventory_update.low_stock_threshold, inventory_update.note)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/transactions", response_model=List[InventoryTransaction])
def get_inventory_transactions(product_id: Optional[int] = None,transaction_type: Optional[str] = None,skip: int = 0,limit: int = 100,db: Session = Depends(get_db)):
    return inventory_service.get_inventory_transactions(db, product_id, transaction_type, skip, limit)