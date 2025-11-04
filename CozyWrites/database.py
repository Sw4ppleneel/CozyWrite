import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# prefer a single DATABASE_URL (recommended on Render). Fallback to parts.
database_url = os.getenv("DATABASE_URL")
if not database_url:
    host = settings.DATABASE_HOSTNAME
    user = settings.DATABASE_USERNAME
    password = settings.DATABASE_PASSWORD
    dbname = settings.DATABASE_NAME
    # include sslmode=require for managed DBs that require TLS
    database_url = f"postgresql+psycopg://{user}:{password}@{host}:5432/{dbname}"

# DEBUG: print masked URL (remove before production)
_masked = database_url.replace(settings.DATABASE_PASSWORD, "*****") if settings.DATABASE_PASSWORD else database_url
print("Using database URL:", _masked)

engine = create_engine(database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
