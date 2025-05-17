# E-commerce Admin API for FORSIT Backend test
A backend API I built for managing e-commerce operations. This helps admin users track sales, manage inventory, and analyze revenue across different marketplaces.

## What will it do.

### Sales and Analytics
- Track sales with filters (date ranges, products, categories, etc.)
- Break down revenue by day/week/month/year
- Compare performance between time periods
- See which marketplaces are performing best

### Inventory Stuff
- Keep tabs on stock levels
- Get alerts when items are running low
- Track inventory history (who changed what and when)
- See stock movement patterns over time

### Product Management
- Basic CRUD for products
- Organize with categories
- See which products actually sell

## Technology Stack

- **Python 3.8 or plus** 
- **FastAPI**  
- **SQLAlchemy** 
- **Pydantic** 
- **MySQL** 
- **Uvicorn**


### Products
- `GET /api/products` - list products (with pagination)
- `GET /api/products/{id}` - Get a product
- `POST /api/products` - create product
- `PUT /api/products/{id}` -update product
- `DELETE /api/products/{id}` - Soft delete or just marks inactive

### Inventory
- `GET /api/inventory` - Current inventory status
- `GET /api/inventory/low-stock` - What needs restocking
- `PUT /api/inventory/{id}` - Update stock levels
- `GET /api/inventory/transactions` - Audit trail of changes

### Sales
- `GET /api/sales/orders` - Order list with filters
- `GET /api/sales/orders/{id}` - Order details
- `POST /api/sales/orders` - Create order (mostly for testing)
- `PUT /api/sales/orders/{id}/status` - Update status

### Analytics
- `GET /api/analytics/revenue` - Revenue breakdown with period grouping
- `GET /api/analytics/sales-by-category` - Category performance
- `GET /api/analytics/marketplace-performance` - Amazon vs Walmart vs direct

## Database Design

I went with a standard relational model:

- **Categories** -> **Products** -> **Inventory**
- **Orders** -> **Order Items**
- **Inventory Transactions** (for audits)

Added indexes on the fields we query most often (order dates, product references, etc.) to keep things fast when the DB grows.

## Setting It Up

### You'll Need
- Python 3.8+
- MySQL 5.7+

### Steps
1. Clone it
```bash
git clone https://github.com/yourusername/ecommerce-admin-api.git
cd ecommerce-admin-api
```

2. Set up venv (always use a venv!)
```bash
python -m venv venv
venv\Scripts\activate.bat  # Windows
```

3. Install deps
```bash
pip install -r requirements.txt
```

4. Fix the DB connection in `database.py` 
   - You'll need to change username/password to match your setup
   - MySQL throws a fit with special chars in passwords, so watch out for that

5. Load some test data
```bash
python demo_data.py
```

6. Fire it up
```bash
uvicorn main:app --reload
```

Check http://localhost:8000/docs to see the interactive API docs.

## Test Data

The demo script creates:
- 5 product categories
- 25 products (5 per category)
- ~100 random orders spread across the last 3 months
- Inventory levels (some items deliberately set low)

This gives you enough realistic data to actually test the analytics features.

## Known Issues & TODOs

- The analytics queries will get slow with a lot of data - needs optimization
- No auth yet - I'd add JWT in a real production version
- Connection pooling is basic - would improve for high traffic
- Error handling could be more robust in some edge cases

## Deps

```
fastapi==0.95.1
uvicorn==0.22.0
sqlalchemy==2.0.12
pymysql==1.0.3
python-dotenv==1.0.0
pydantic==1.10.7
```

## License

MIT - Do whatever you want with it.