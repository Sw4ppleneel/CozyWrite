from .. import schemas , Models , database 
from sqlalchemy.orm import Session
from ..database import get_db
from fastapi import Body, FastAPI, Response, status, HTTPException , Depends , APIRouter
from ..oauth2 import get_current_user  # or whatever symbol(s) you need

# creating a user , hashing the password
import hashlib

def hash_data(data_string, algorithm='sha256'):
    hasher = getattr(hashlib, algorithm)()
    hasher.update(data_string.encode('utf-8'))
    return hasher.hexdigest()

router = APIRouter()


#create new user 
@router.post("/users" , status_code=status.HTTP_201_CREATED , response_model=
          schemas.returnUser)
def createUser(user : schemas.userCreate , db : Session = Depends(get_db)):
    hashed_password = hash_data(user.password)
    user.password = hashed_password
    newusr = Models.User(**user.dict())
    db.add(newusr)
    db.commit()
    db.refresh(newusr)

    return newusr

#refrence password context accha   


@router.get("/user/{id}" , response_model = schemas.returnUser)
def get_usr(id : int , db : Session = Depends(get_db)):
    usr = db.query(Models.User).filter(Models.User.id == id).first()
    if usr is None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail= "Not Found")
    return usr