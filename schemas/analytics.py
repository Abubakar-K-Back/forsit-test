from typing import List, Optional
from datetime import date
from pydantic import BaseModel, Field

class RevenuePoint(BaseModel):
    period: str
    revenue: float
    order_count: int
    average_order_value: float

class RevenueAnalytics(BaseModel):
    total_revenue: float
    average_order_value: float
    data_points: List[RevenuePoint]

class CategorySales(BaseModel):
    category_id: int
    category_name: str
    total_sales: float
    order_count: int
    product_count: int

class CategorySalesResponse(BaseModel):
    total_sales: float
    data: List[CategorySales]

class ProductSales(BaseModel):
    product_id: int
    sku: str
    name: str
    total_sales: float
    units_sold: int