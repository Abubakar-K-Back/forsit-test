from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from models.product import Product, Category
from schemas.product import ProductCreate, ProductUpdate, CategoryCreate

def get_products(db: Session, skip: int = 0, limit: int = 100, category_id: Optional[int] = None) -> List[Product]:
    query = db.query(Product).filter(Product.is_active == True)
    
    if category_id:
        query = query.filter(Product.category_id == category_id)
    
    return query.offset(skip).limit(limit).all()

def get_product(db: Session, product_id: int) -> Optional[Product]:
    return db.query(Product).filter(
        Product.id == product_id,
        Product.is_active == True
    ).first()

def create_product(db: Session, product_data: ProductCreate) -> Product:
    #Creating a new product
    db_product = Product(**product_data.dict())
    db.add(db_product)
    
    try:
        db.commit()
        db.refresh(db_product)
        return db_product
    except IntegrityError:
        db.rollback()
        raise ValueError("Product with this SKU number already exists in db.")

def update_product(
    db: Session, 
    product_id: int, 
    product_data: ProductUpdate
) -> Optional[Product]:
    db_product = db.query(Product).filter(Product.id == product_id).first()
    
    if not db_product:
        return None
    
    # Update product attributes
    for key, value in product_data.dict(exclude_unset=True).items():
        setattr(db_product, key, value)
    
    db.commit()
    db.refresh(db_product)
    return db_product

# we dont want to delete whole product so for now we are setting availble state to false.
def delete_product(db: Session, product_id: int) -> bool:
    db_product = db.query(Product).filter(Product.id == product_id).first()
    
    if not db_product:
        return False
    
    db_product.is_active = False
    db.commit()
    return True

def get_categories(db: Session) -> List[Category]:
    return db.query(Category).all()

def create_category(db: Session, category_data: CategoryCreate) -> Category:
    db_category = Category(**category_data.dict())
    db.add(db_category)
    try:
        db.commit()
        db.refresh(db_category)
        return db_category
    except IntegrityError:
        db.rollback()
        raise ValueError("Category with this name already exists")