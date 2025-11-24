import fastapi
from fastapi import APIRouter, Depends, HTTPException, Response, status
from .. import oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from ..schemas import user_login
from .. import schemas
from .. import Models
from .. import utils
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=['Authentication'])

@router.post("/login", response_model=schemas.token)
def login(user_creds: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(Models.User).filter(Models.User.email == user_creds.username).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials"
        )
    
    if not utils.verify(user_creds.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials"
        )
    
    # Create access token
    access_token = oauth2.create_access_token(data={"userid": user.id})
    
    return {"access_token": access_token, "token_type": "bearer"}


