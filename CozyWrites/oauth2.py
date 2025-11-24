import fastapi 
from fastapi import APIRouter, Depends, HTTPException, status
from jose import jwt
from jose.exceptions import JWTError
from datetime import datetime, timedelta
from . import schemas
from fastapi.security import OAuth2PasswordBearer
from . import database
from sqlalchemy.orm import Session
from . import Models
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        id: str = payload.get("userid")
        
        if id is None:
            raise credentials_exception
            
        token_data = schemas.tokenData(id=id)
        return token_data
        
    except JWTError:
        raise credentials_exception

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not verify credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    
    token_data = verify_token(token, credentials_exception)
    user = db.query(Models.User).filter(Models.User.id == token_data.id).first()
    
    if user is None:
        raise credentials_exception
        
    return user
