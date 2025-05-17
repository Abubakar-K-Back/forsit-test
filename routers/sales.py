from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import get_db
from schemas.sales import Order, OrderCreate
from services import sales_service

router = APIRouter(prefix="/api/sales", tags=["sales"])

@router.get("/orders", response_model=List[Order])
def get_orders(marketplace: Optional[str] = None, status: Optional[str] = None, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return sales_service.get_orders(db, marketplace, status, start_date, end_date, skip, limit)

@router.get("/orders/{order_id}", response_model=Order)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = sales_service.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.post("/orders", response_model=Order)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    return sales_service.create_order(db, order)

@router.put("/orders/{order_id}/status", response_model=Order)
def update_order_status(order_id: int, status: str = Query(..., description="New order status"), db: Session = Depends(get_db)):
    order = sales_service.update_order_status(db, order_id, status)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order