from pydantic import BaseModel , EmailStr 
from datetime import datetime
from typing import Optional, Annotated
from pydantic import Field
from sqlalchemy.orm import relationship



# defining a pydantic model
class Post(BaseModel):
    Title: str
    Content: str
    Published: bool = True

class PostCreate(Post):

    pass

class returnUser(BaseModel):
    email : EmailStr
    id : int 
    Created_at : datetime
    class Config:
        orm_mode = True

class Response(BaseModel):
    Title : str
    Content : str
    Published : bool
    id : int
    user_id : int
    owner : returnUser
    class Config:
        orm_mode = True

class userCreate(BaseModel):
    email : EmailStr
    password : str 
    class Config:
        orm_mode = True



class user_login(BaseModel):
    email : EmailStr
    password : str
    class Config : 
        orm_mode = True


class token(BaseModel):
    access_token : str
    token_type : str

class tokenData(BaseModel):
    id : Optional[int]


class Votes(BaseModel) : 
    post_id: int
    dir: Annotated[int, Field(ge=-1, le=1)]


class PostOut(BaseModel):
    post : Response
    votes : int
    class Config:
        orm_mode = True
