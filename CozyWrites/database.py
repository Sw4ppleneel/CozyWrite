import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

sql_alchemy_db_url = f'postgresql+psycopg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}'

engine = create_engine(sql_alchemy_db_url)
SessionLocal = sessionmaker(autocommit=False , autoflush=False , bind=engine)


#sql_alchemy_db_url = 'postgresql://<username>:<pass>@<ip_address/hostname>/<dbname>'

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 
