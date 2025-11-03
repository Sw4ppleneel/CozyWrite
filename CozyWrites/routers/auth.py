import fastapi
from fastapi import APIRouter , Depends , HTTPException , Response ,status
import hashlib  
from .. import oauth2
from ..database import get_db
from sqlalchemy.orm  import Session
from ..schemas import user_login
from .. import schemas
from ..import Models
from ..import utils
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
router= APIRouter()

def hash_data(data_string, algorithm='sha256'):
    hasher = getattr(hashlib, algorithm)()
    hasher.update(data_string.encode('utf-8'))
    return hasher.hexdigest()

@router.post("/login" , response_model=schemas.token)
def login( user_creds : OAuth2PasswordRequestForm = Depends() , db : Session = Depends(get_db)):
   user = db.query(Models.User).filter(Models.User.email == user_creds.username).first()
   if not user :
       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail= "Invalid Credentials")
   
   if utils.verify(user_creds.password , user.password) == 0 :
       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail= "Invalid")
   
   access_token = oauth2.create_access_token(data={"userid": user.id})  # fix name if needed
   return {"access_token": access_token, "token_type": "bearer"}


