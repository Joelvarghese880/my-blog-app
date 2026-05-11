from datetime import datetime
from pydantic import BaseModel,ConfigDict,Field,EmailStr


class UserCreate(BaseModel):
    username: str = Field(min_length=3,max_length=50)
    email: EmailStr
    password: str = Field(min_length=6,max_length=255)


class UserResponse(BaseModel):
    id : int
    username: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str


class PostBase(BaseModel):
    title: str = Field(min_length=1,max_length=50)
    content: str = Field(min_length=1)


class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    author: UserResponse
    
    model_config = ConfigDict(from_attributes=True)