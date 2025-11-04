import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# prefer a single DATABASE_URL (useful on Render); fallback to individual parts
database_url = os.getenv("DATABASE_URL")
if not database_url:
    database_url = (
        f"postgresql+psycopg://{settings.database_username}:"
        f"{settings.database_password}@{settings.database_hostname}/{settings.database_name}"
    )

engine = create_engine(database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
