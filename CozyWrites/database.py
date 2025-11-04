import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# prefer a single DATABASE_URL (recommended on Render). Fallback to parts.
database_url = os.getenv("DATABASE_URL")
if not database_url:
    # build URL from the mapped env vars (note uppercase names used in Settings)
    host = settings.DATABASE_HOSTNAME
    user = settings.DATABASE_USERNAME
    password = settings.DATABASE_PASSWORD
    dbname = settings.DATABASE_NAME
    # add sslmode=require if your hosted DB requires TLS (common on managed hosts)
    database_url = f"postgresql+psycopg://{user}:{password}@{host}:5432/{dbname}?sslmode=require"

# debug: show effective host (mask password) — remove after debugging
_debug_url = database_url.replace(settings.DATABASE_PASSWORD, "*****") if hasattr(settings, "DATABASE_PASSWORD") else database_url
print("Using database URL:", _debug_url)

# create engine
engine = create_engine(database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
