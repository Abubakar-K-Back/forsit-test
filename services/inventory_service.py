from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_

from models.inventory import Inventory, InventoryTransaction
from models.product import Product

def get_all_inventory(db: Session, skip: int = 0, limit: int = 100) -> List[Inventory]:
    return db.query(Inventory).offset(skip).limit(limit).all()

def get_product_inventory(db: Session, product_id: int) -> Optional[Inventory]:
    #Get inventory for a particular productl.
    return db.query(Inventory).filter(Inventory.product_id == product_id).first()

def get_low_stock_products(db: Session) -> List[dict]:
    results = []
    
    # Get inventory items below threshold with related product info
    low_stock_items = (
        db.query(
            Inventory.product_id, 
            Inventory.quantity, 
            Inventory.low_stock_threshold,
            Product.sku,
            Product.name
        ).join(Product, Inventory.product_id == Product.id).filter(and_(
                Product.is_active == True,
                Inventory.quantity < Inventory.low_stock_threshold
            )).all()
    )
    
    # Format for response
    for item in low_stock_items:
        results.append({
            "product_id": item.product_id,
            "sku": item.sku,
            "name": item.name,
            "current_quantity": item.quantity,
            "low_stock_threshold": item.low_stock_threshold
        })
    
    return results

def update_inventory(
    db: Session, 
    product_id: int, 
    new_quantity: int,
    low_stock_threshold: Optional[int] = None,
    note: Optional[str] = None
) -> Inventory:
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id).first()
    
    if not inventory:
        raise ValueError(f"No inventory data found for product ID : {product_id}")
    quantity_change = new_quantity - inventory.quantity
    transaction = InventoryTransaction(
        product_id=product_id,
        quantity_change=quantity_change,
        transaction_type="adjustment",
        note=note,
        created_at=datetime.now()
    )
    inventory.quantity = new_quantity
    
    if low_stock_threshold is not None:
        inventory.low_stock_threshold = low_stock_threshold
    
    if quantity_change > 0:
        inventory.last_restock_date = datetime.now()
    
    db.add(transaction)
    db.commit()
    db.refresh(inventory)
    
    return inventory

def get_inventory_transactions(db: Session, product_id: Optional[int] = None, transaction_type: Optional[str] = None, skip: int = 0, limit: int = 100) -> List[InventoryTransaction]:
    query = db.query(InventoryTransaction)
    
    if product_id:
        query = query.filter(InventoryTransaction.product_id == product_id)
    
    if transaction_type:
        query = query.filter(InventoryTransaction.transaction_type == transaction_type)
    
    return query.order_by(InventoryTransaction.created_at.desc()).offset(skip).limit(limit).all()