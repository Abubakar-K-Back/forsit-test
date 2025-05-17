from sqlalchemy import Column, Integer, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import relationship

from database import Base
from models.base import TimestampMixin

class Inventory(Base, TimestampMixin):
    __tablename__ = "inventory"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), unique=True)
    quantity = Column(Integer, default=0)
    low_stock_threshold = Column(Integer, default=10)
    last_restock_date = Column(DateTime, nullable=True)    
    product = relationship("Product", back_populates="inventory")

class InventoryTransaction(Base):
    __tablename__ = "inventory_transactions"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity_change = Column(Integer, nullable=False)
    transaction_type = Column(String(20), nullable=False)  # purchase, sale, adjustment, return
    reference_id = Column(String(100), nullable=True)
    note = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False)