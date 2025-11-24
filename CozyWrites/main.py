from fastapi import Body, FastAPI, Response, status, HTTPException , Depends
from pydantic import BaseModel, Field
from random import randrange
from datetime import datetime
import hashlib
import psycopg
from sqlalchemy.orm import Session 
import time
from . import Models , schemas
from .database import engine , SessionLocal
from pydantic_settings import BaseSettings
from pathlib import Path
from .config import Settings
from fastapi.middleware.cors import CORSMiddleware





settings = Settings()


#hashing algorithm
def hash_data(data_string, algorithm='sha256'):
    hasher = getattr(hashlib, algorithm)()
    hasher.update(data_string.encode('utf-8'))
    return hasher.hexdigest()



#Imports the model into the binded db through the url
Models.Base.metadata.create_all(bind = engine)


#Session is responsible for talking to the db 




app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# while True:
#     try:
#         conn = psycopg.connect(host='localhost', dbname = 'fastapi', user='postgres', password='sw4pneel', port = 5432)
#         cursor = conn.cursor(row_factory=psycopg.rows.dict_row)
#         print("Database connection was successful!")

#         # ensure SQLAlchemy tables exist after DB is reachable
#         try:
#             Models.Base.metadata.create_all(bind=engine)
#         except Exception as e:
#             print("Warning: create_all failed:", e)

#         break
#     except Exception as e:
#         print("Error connecting to the database:", e)
#         time.sleep(2)

# root path
@app.get("/")
def read_root():
    return {"Hello": "Welcome to CozyWrites , Login at /docs for API documentation!"}

from .routers import users, posts, auth , vote  # or: from .routers import users, posts; from .routers import auth


app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)
