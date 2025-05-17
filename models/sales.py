from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship

from database import Base
from models.base import TimestampMixin

class Order(Base, TimestampMixin):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(50), unique=True, index=True)
    order_date = Column(DateTime, index=True)
    status = Column(String(20), index=True)  # pending, processing, shipped, delivered, cancelled
    payment_status = Column(String(20))  # pending, paid, failed, refunded
    subtotal = Column(Float, nullable=False)
    tax = Column(Float, nullable=False)
    shipping_cost = Column(Float, nullable=False)
    discount = Column(Float, default=0.0)
    total = Column(Float, nullable=False)
    marketplace = Column(String(20), index=True)  # amazon, walmart, direct
    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)
    created_at = Column(DateTime, nullable=False)
    
    # Relationships
    order = relationship("Order", back_populates="items")
    product = relationship("Product")