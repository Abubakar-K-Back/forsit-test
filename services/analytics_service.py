from typing import List, Dict, Any
from datetime import date, datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, extract
from sqlalchemy.sql import label

from models.sales import Order, OrderItem
from models.product import Product, Category

def get_revenue_by_period(db: Session, start_date: date, end_date: date, group_by: str = "day") -> Dict[str, Any]:
    start_datetime = datetime.combine(start_date, datetime.min.time())
    end_datetime = datetime.combine(end_date, datetime.max.time())
    query_totals = db.query(
        func.sum(Order.total).label("total_revenue"),
        func.count(Order.id).label("order_count")
    ).filter(
        Order.order_date.between(start_datetime, end_datetime)
    ).first()
    
    total_revenue = query_totals.total_revenue or 0
    order_count = query_totals.order_count or 0
    avg_order_value = total_revenue / order_count if order_count > 0 else 0
    
    if group_by == "day":
        # For simplicity, use date part of order_date
        date_format = func.date(Order.order_date)
    elif group_by == "week":
        date_format = func.date_format(Order.order_date, '%Y-%u')
    elif group_by == "month":
        date_format = func.date_format(Order.order_date, '%Y-%m')
    elif group_by == "year":
        date_format = func.extract('year', Order.order_date)
    else:
        raise ValueError(f"Invalid groupby parameter: {group_by}")
    
    query_by_period = db.query(
        date_format.label("period"),
        func.sum(Order.total).label("revenue"),
        func.count(Order.id).label("order_count")
    ).filter(
        Order.order_date.between(start_datetime, end_datetime)
    ).group_by("period").order_by("period").all()
    
    data_points = []
    for point in query_by_period:
        period_revenue = point.revenue or 0
        period_orders = point.order_count or 0
        period_avg = period_revenue / period_orders if period_orders > 0 else 0
        
        data_points.append({
            "period": str(point.period),
            "revenue": float(period_revenue),
            "order_count": period_orders,
            "average_order_value": float(period_avg)
        })
    
    return {
        "total_revenue": float(total_revenue),
        "average_order_value": float(avg_order_value),
        "data_points": data_points
             }

def get_sales_by_category(db: Session, start_date: date, end_date: date) -> Dict[str, Any]:
    start_datetime = datetime.combine(start_date, datetime.min.time())
    end_datetime = datetime.combine(end_date, datetime.max.time())
    
    # this query is for the category sales e.g. by name by category id...
    category_sales = db.query(
        Category.id.label("category_id"),
        Category.name.label("category_name"),
        func.sum(OrderItem.subtotal).label("total_sales"),
        func.count(OrderItem.id.distinct()).label("order_count"),
        func.count(OrderItem.product_id.distinct()).label("product_count")
    ).join(
        Product, Product.id == OrderItem.product_id
    ).join(
        Category, Category.id == Product.category_id
    ).join(
        Order, Order.id == OrderItem.order_id
    ).filter(
        Order.order_date.between(start_datetime, end_datetime)
    ).group_by(
        Category.id, Category.name
    ).all()
    total_sales = sum(float(item.total_sales or 0) for item in category_sales)
    
    result = {
        "total_sales": total_sales,
        "data": []
    }
    
    for item in category_sales:
        result["data"].append({
            "category_id": item.category_id,
            "category_name": item.category_name,
            "total_sales": float(item.total_sales or 0),
            "order_count": item.order_count,
            "product_count": item.product_count
        })
    
    return result

def get_marketplace_performance(db: Session, start_date: date, end_date: date) -> Dict[str, Any]:
    start_datetime = datetime.combine(start_date, datetime.min.time())
    end_datetime = datetime.combine(end_date, datetime.max.time())
    
    marketplace_data = db.query(Order.marketplace,func.sum(Order.total).label("total_sales"),func.count(Order.id).label("order_count"),func.avg(Order.total).label("average_order_value")
    ).filter(Order.order_date.between(start_datetime, end_datetime)).group_by(Order.marketplace).all()
    
    result = {
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "marketplaces": []
    }
    
    for item in marketplace_data:
        result["marketplaces"].append({
            "name": item.marketplace,
            "total_sales": float(item.total_sales or 0),
            "order_count": item.order_count,
            "average_order_value": float(item.average_order_value or 0)
        })
    
    return result