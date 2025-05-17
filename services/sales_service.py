from typing import List, Optional
from datetime import datetime
import uuid
from sqlalchemy.orm import Session
from sqlalchemy import and_

from models.sales import Order, OrderItem
from models.inventory import Inventory, InventoryTransaction
from schemas.sales import OrderCreate

def get_orders(
    db: Session,
    marketplace: Optional[str] = None,
    status: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    skip: int = 0,
    limit: int = 100
) -> List[Order]:
    query = db.query(Order)
    
    if marketplace:
        query = query.filter(Order.marketplace == marketplace)
    if status:
        query = query.filter(Order.status == status)
    if start_date and end_date:
        query = query.filter(Order.order_date.between(start_date, end_date))
    elif start_date:
        query = query.filter(Order.order_date >= start_date)
    elif end_date:
        query = query.filter(Order.order_date <= end_date)
    
    return query.order_by(Order.order_date.desc()).offset(skip).limit(limit).all()

#get order by id
def get_order(db: Session, order_id: int) -> Optional[Order]:
    return db.query(Order).filter(Order.id == order_id).first()

def create_order(db: Session, order_data: OrderCreate) -> Order:
    order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
    db_order = Order(
        order_number=order_number,
        order_date=order_data.order_date,
        status=order_data.status,
        payment_status=order_data.payment_status,
        subtotal=order_data.subtotal,
        tax=order_data.tax,
        shipping_cost=order_data.shipping_cost,
        discount=order_data.discount,
        total=order_data.total,
        marketplace=order_data.marketplace
    )
    db.add(db_order)
    db.flush()  # Flush to get the order ID
    
    # Create order items
    for item_data in order_data.items:
        order_item = OrderItem(
            order_id=db_order.id,
            product_id=item_data.product_id,
            quantity=item_data.quantity,
            unit_price=item_data.unit_price,
            subtotal=item_data.quantity * item_data.unit_price,
            created_at=order_data.order_date
        )
        db.add(order_item)
        if order_data.status != "cancelled":
            inventory = db.query(Inventory).filter(
                Inventory.product_id == item_data.product_id
            ).first()
            
            if inventory:
                inventory.quantity = max(0, inventory.quantity - item_data.quantity)
                transaction = InventoryTransaction(
                    product_id=item_data.product_id,
                    quantity_change=-item_data.quantity,
                    transaction_type="sale",
                    reference_id=order_number,
                    created_at=order_data.order_date
                )
                db.add(transaction)
    
    db.commit()
    db.refresh(db_order)
    return db_order

def update_order_status(db: Session, order_id: int, new_status: str) -> Optional[Order]:
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        return None
    old_status = db_order.status
    db_order.status = new_status    
    if old_status != new_status:
        # If order was not cancelled but is now cancelled, restore inventory
        if old_status != "cancelled" and new_status == "cancelled":
            order_items = db.query(OrderItem).filter(OrderItem.order_id == order_id).all()
            
            for item in order_items:
                inventory = db.query(Inventory).filter(
                    Inventory.product_id == item.product_id
                ).first()
                
                if inventory:
                    inventory.quantity += item.quantity
                    
                    transaction = InventoryTransaction(
                        product_id=item.product_id,
                        quantity_change=item.quantity,
                        transaction_type="adjustment",
                        reference_id=db_order.order_number,
                        note=f"Order cancelled: {db_order.order_number}",
                        created_at=datetime.now()
                    )
                    db.add(transaction)
        
        # If order was cancelled but is now not cancelled, reduce inventory
        elif old_status == "cancelled" and new_status != "cancelled":
            order_items = db.query(OrderItem).filter(OrderItem.order_id == order_id).all()
            
            for item in order_items:
                inventory = db.query(Inventory).filter(
                    Inventory.product_id == item.product_id
                ).first()
                
                if inventory:
                    # Reduce inventory
                    inventory.quantity = max(0, inventory.quantity - item.quantity)
                    
                    #create inventory transaction
                    transaction = InventoryTransaction(
                        product_id=item.product_id,
                        quantity_change=-item.quantity,
                        transaction_type="sale",
                        reference_id=db_order.order_number,
                        note=f"Order status changed from cancelled to {new_status}",
                        created_at=datetime.now()
                    )
                    db.add(transaction)
    
    db.commit()
    db.refresh(db_order)
    return db_order