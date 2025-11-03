import fastapi 
from fastapi import APIRouter, Depends, HTTPException, status
from jose import jwt
from jose.exceptions import JWTError
from datetime import datetime , timedelta

import sqlalchemy
from . import schemas
from fastapi import Depends , HTTPException
from fastapi.security import OAuth2PasswordBearer
from . import database
from sqlalchemy.orm import Session
from . import Models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_TIME_MINUTES = 30

def create_access_token(data : dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_TIME_MINUTES)
    to_encode.update({"exp" : expire })

    encoded_jwt = jwt.encode(to_encode , SECRET_KEY ,algorithm= ALGORITHM )

    return encoded_jwt


def verify_token(token : str , credentials_exception ):
 try:
     payload =  jwt.decode (token , SECRET_KEY , algorithms=ALGORITHM)
     id = payload.get("userid")
     if id is None :
         raise credentials_exception
     token_data = schemas.tokenData(id=id)

     return token_data
        
 except JWTError :
    raise credentials_exception
 

def get_current_user(token : str = Depends(oauth2_scheme) , db : Session = Depends (database.get_db)):
   credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , 
                                         detail= "Could not verify" ,
                                           headers={"WWW-Authenticate" : "Bearer"})

   user = db.query(Models.User).filter(Models.User.id == verify_token(token , credentials_exception).id).first()
   return user
