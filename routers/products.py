from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import get_db
from schemas.product import Product, ProductCreate, ProductUpdate, Category, CategoryCreate
from services import product_service

router = APIRouter(prefix="/api/products", tags=["products"])

# Product endpoints
@router.get("/", response_model=List[Product])
def get_products(skip: int = 0, limit: int = 100, category_id: Optional[int] = None, db: Session = Depends(get_db)):
    return product_service.get_products(db, skip, limit, category_id)

@router.get("/{product_id}", response_model=Product)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = product_service.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/", response_model=Product)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    return product_service.create_product(db, product)

@router.put("/{product_id}", response_model=Product)
def update_product(product_id: int, product_update: ProductUpdate, db: Session = Depends(get_db)):
    product = product_service.update_product(db, product_id, product_update)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.delete("/{product_id}", response_model=dict)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    success = product_service.delete_product(db, product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"success": True, "message": "Product deleted successfully"}

# Category routes
@router.get("/categories/", response_model=List[Category])
def get_categories(db: Session = Depends(get_db)):
    return product_service.get_categories(db)

@router.post("/categories/", response_model=Category)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    return product_service.create_category(db, category)