import random
from datetime import datetime, timedelta
import uuid
import sys
from sqlalchemy.orm import Session

# Add the parent directory to sys.path to allow importing the app
sys.path.append("..")

from database import SessionLocal, engine, Base
from models.product import Category, Product
from models.inventory import Inventory, InventoryTransaction
from models.sales import Order, OrderItem

# Create database tables if they don't exist
Base.metadata.create_all(bind=engine)

# Sample data
CATEGORIES = [
    {"name": "Electronics", "description": "Electronic devices and accessories"},
    {"name": "Clothing", "description": "Apparel and fashion items"},
    {"name": "Home & Kitchen", "description": "Home appliances and kitchenware"},
    {"name": "Books", "description": "Books and publications"},
    {"name": "Toys & Games", "description": "Toys, games, and entertainment items"}
]

# Product data by category
PRODUCTS = {
    "Electronics": [
        {"name": "Wireless Headphones", "price": 112.99, "description": "Noise-cancelling wireless headphones"},
        {"name": "Smart Watch", "price": 193.99, "description": "Fitness and health tracking smartwatch"},
        {"name": "Bluetooth Speaker", "price": 72.99, "description": "Portable Bluetooth speaker with bass boost"},
        {"name": "USB-C Charger", "price": 24.95, "description": "Fast charging USB-C power adapter"},
        {"name": "Wireless Mouse", "price": 39.29, "description": "Ergonomic wireless mouse"}
    ],
    "Clothing": [
        {"name": "Men's T-Shirt", "price": 19.51, "description": "cotton crew neck t-shirt"},
        {"name": "Women's Jeans", "price": 49.66, "description": "slim fit denim jeans"},
        {"name": "Winter Jacket", "price": 89.22, "description": " Waterproof insulated winter jacket"},
        {"name": "Running Shoes", "price": 79.92, "description": "lightweight running shoes"},
        {"name": "Baseball Cap", "price": 12.19, "description": "adjustable cotton baseball cap"}
    ],
    "Home & Kitchen": [
        {"name": "Coffee Maker", "price": 69.99, "description": "programmable drip coffee maker"},
        {"name": "Toaster", "price": 34.99, "description": "2 slice stainless steel toaster"},
        {"name": "Blender", "price": 49.99, "description": "High performance countertop blender"},
        {"name": "Knife Set", "price": 59.99, "description": "8 piece stainless steel knife set"},
        {"name": "Non-stick Pan", "price": 29.99, "description": "10 inch non-stick frying pan"}
    ],
    "Books": [
        {"name": "Python Programming", "price": 39.39, "description": "Comprehensive guide to Python programming"},
        {"name": "Data Science Handbook", "price": 49.91, "description": "essential handbook for data scientists"},
        {"name": "Fiction Bestseller", "price": 24.59, "description": "award-winning fiction novel"},
        {"name": "Cookbook", "price": 34.99, "description": "Collection of 100 recipes"},
        {"name": "Business Strategy", "price": 29.29, "description": "business strategy and leadership book"}
    ],
    "Toys & Games": [
        {"name": "Board Game", "price": 29.99, "description": "Family board game"},
        {"name": "LEGOSet", "price": 59.99, "description": "Building blocks set"},
        {"name": "Puzzle", "price": 19.99, "description": "1000 piece jigsaw puzzle"},
        {"name": "Remote Control Car", "price": 19.99, "description": "RC offroad vehicle"},
        {"name": "Action Figure", "price": 64.99, "description": "Collectible action figure"}
    ]
}

# Marketplace options
MARKETPLACES = ["amazon", "walmart", "direct"]

# Order status options
ORDER_STATUS = ["pending", "processing", "shipped", "delivered", "cancelled"]
PAYMENT_STATUS = ["pending", "paid", "failed", "refunded"]

def generate_sku(category_name, product_name):
    """Generate a unique SKU based on category and product name"""
    category_prefix = ''.join([word[0] for word in category_name.split()]).upper()
    product_prefix = ''.join([word[0] for word in product_name.split()]).upper()
    random_suffix = str(random.randint(1000, 9999))
    return f"{category_prefix}-{product_prefix}-{random_suffix}"

def create_demo_data():
    db = SessionLocal()
    try:
        # Check if data already exists
        existing_categories = db.query(Category).count()
        if existing_categories > 0:
            print("Data already exists in the database so skipping the insertion of demo data")
            return
        
        print("Generating demo data")
        
        # Create categories
        db_categories = {}
        for category_data in CATEGORIES:
            category = Category(**category_data)
            db.add(category)
            db.flush()  # Flush to get the ID
            db_categories[category.name] = category.id
        
        # Create products with inventory
        db_products = []
        for category_name, products in PRODUCTS.items():
            category_id = db_categories[category_name]
            
            for product_data in products:
                # Create product
                product = Product(
                    sku=generate_sku(category_name, product_data["name"]),
                    name=product_data["name"],
                    description=product_data["description"],
                    price=product_data["price"],
                    category_id=category_id,
                    image_url=f"https://example.com/rand/images/{product_data['name'].lower().replace(' ', '-')}.jpg",
                    is_active=True
                )
                db.add(product)
                db.flush()  # Flush to get the ID
                
                # Create inventory
                inventory = Inventory(product_id=product.id, quantity=random.randint(5, 100), low_stock_threshold=10, last_restock_date=datetime.now() - timedelta(days=random.randint(1, 30)))
                db.add(inventory)
                
                # Add to product list for order generation
                db_products.append((product.id, product.price))
        
        # Create orders with order items
        for _ in range(100):  # Generate 100 orders
            # Randomize order date within the last 3 months
            order_date = datetime.now() - timedelta(days=random.randint(1, 90))
            
            # Generate random order data
            subtotal = 0
            items = []
            
            # Add 1-5 items to the order
            for _ in range(random.randint(1, 5)):
                product_id, price = random.choice(db_products)
                quantity = random.randint(1, 3)
                item_subtotal = price * quantity
                subtotal += item_subtotal
                
                items.append({
                    "product_id": product_id,
                    "quantity": quantity,
                    "unit_price": price,
                    "subtotal": item_subtotal
                })
            
            # Calculate order totals
            tax = round(subtotal * 0.08, 2)  # 8% tax
            shipping = 5.99 if subtotal < 50 else 0  # Free shipping over $50
            discount = round(subtotal * random.choice([0, 0, 0, 0.05, 0.1]), 2)  # Random discount
            total = subtotal + tax + shipping - discount
            
            # Create order
            order = Order(
                order_number=f"ORD-{uuid.uuid4().hex[:8].upper()}",
                order_date=order_date,
                status=random.choice(ORDER_STATUS),
                payment_status=random.choice(PAYMENT_STATUS),
                subtotal=subtotal,
                tax=tax,
                shipping_cost=shipping,
                discount=discount,
                total=total,
                marketplace=random.choice(MARKETPLACES),
                created_at=order_date,
                updated_at=order_date
            )
            db.add(order)
            db.flush()  # Flush to get the ID
            
            for item_data in items:
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=item_data["product_id"],
                    quantity=item_data["quantity"],
                    unit_price=item_data["unit_price"],
                    subtotal=item_data["subtotal"],
                    created_at=order_date
                )
                db.add(order_item)
                
                inventory = db.query(Inventory).filter(
                    Inventory.product_id == item_data["product_id"]
                ).first()
                
                if inventory and order.status != "cancelled":
                    # Reduce inventory for non-cancelled orders
                    inventory.quantity = max(0, inventory.quantity - item_data["quantity"])
                    
                    # Create inventory transaction
                    transaction = InventoryTransaction(
                        product_id=item_data["product_id"],
                        quantity_change=-item_data["quantity"],
                        transaction_type="sale",
                        reference_id=order.order_number,
                        created_at=order_date
                    )
                    db.add(transaction)
        
        db.commit()
        print("Demo data generation complete!")
        
    except Exception as e:
        db.rollback()
        print(f"Error generating demo data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_demo_data()