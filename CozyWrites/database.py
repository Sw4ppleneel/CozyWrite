import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# prefer a single DATABASE_URL (recommended on Render). Fallback to parts.
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    host = settings.DATABASE_HOSTNAME
    user = settings.DATABASE_USERNAME
    password = settings.DATABASE_PASSWORD
    dbname = settings.DATABASE_NAME
    # include sslmode=require for managed DBs that require TLS
    DATABASE_URL = f"postgresql+psycopg://{user}:{password}@{host}:5432/{dbname}"


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
