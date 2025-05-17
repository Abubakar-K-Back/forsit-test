from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import urllib.parse

password = "Privaci@123" # we can get password from .env but now pls set password here.
encoded_password = urllib.parse.quote_plus(password)

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://root:{encoded_password}@localhost/ecommerce_admin"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()