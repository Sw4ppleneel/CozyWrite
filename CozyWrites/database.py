import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# Get DATABASE_URL from environment (for Render/Railway/Heroku)
DATABASE_URL = os.getenv("DATABASE_URL")

# Handle different postgres:// prefixes
if DATABASE_URL:
    # Some platforms use postgres:// instead of postgresql://
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg://", 1)
    print(f"Using DATABASE_URL from environment")
else:
    # Fallback to config settings (for Docker Compose and local dev)
    host = settings.DATABASE_HOSTNAME
    user = settings.DATABASE_USERNAME
    password = settings.DATABASE_PASSWORD
    dbname = settings.DATABASE_NAME
    port = settings.DATABASE_PORT
    DATABASE_URL = f"postgresql+psycopg://{user}:{password}@{host}:{port}/{dbname}"
    print(f"Connecting to database at: {host}:{port}/{dbname}")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
