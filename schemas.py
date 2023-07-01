# from ctypes import WinError
import datetime
from pydantic import BaseModel
from typing import List, Optional
from fastapi import Form
from sqlalchemy import Date


class User(BaseModel):
    email: str
    username: str
    password: str
    role: int = 0

class CreateUser(User):
    email: str
    username: str
    password: str

class ShowUser(BaseModel):
    username: str

    class Config():
        orm_mode = True

class Login(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None
    email: Optional[str] = None
    username:Optional[str] = None
    role: Optional[int] = None


class TodoList(BaseModel):
    code:int
    name:str

    class Config:
        orm_mode = True
    

class CheckList(BaseModel):
    # userid:int
    code:int
    done:bool
    date:Optional[datetime.date] = datetime.datetime.today().strftime("%Y-%m-%d")

    class Config:
        orm_mode = True


class ResponseCheckList(BaseModel):
    code:int
    done:bool


# class ResponseMessage(BaseModel):
#     id:int
#     content:str
#     user_id:int
#     chatroom_id:int
#     timestamp:datetime.datetime

#     class config:
#         orm_mode = True