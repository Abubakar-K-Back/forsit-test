from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import get_db
from schemas.analytics import RevenueAnalytics, CategorySalesResponse
from services import analytics_service

router = APIRouter(prefix="/api/analytics", tags=["analytics"])

@router.get("/revenue", response_model=RevenueAnalytics)
def get_revenue_analytics(
    start_date: date,
    end_date: date,
    group_by: str = Query("day", enum=["day", "week", "month", "year"]),
    db: Session = Depends(get_db)
):
    if start_date > end_date:
        raise HTTPException(status_code=400, detail="Start date must be before enddate")
    return analytics_service.get_revenue_by_period(db, start_date, end_date, group_by)

@router.get("/sales-by-category", response_model=CategorySalesResponse)
def get_sales_by_category(start_date: date,end_date: date,db: Session = Depends(get_db)):
    if start_date > end_date:
        raise HTTPException(status_code=400, detail="Start date must be before enddate")
    
    return analytics_service.get_sales_by_category(db, start_date, end_date)

@router.get("/marketplace-performance")
def get_marketplace_performance(start_date: date,end_date: date,db: Session = Depends(get_db)):
    if start_date > end_date:
        raise HTTPException(status_code=400, detail="Start date must be before end date")
    return analytics_service.get_marketplace_performance(db, start_date, end_date)