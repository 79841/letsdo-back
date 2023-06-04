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

class CreateUser(User):
    passwordcheck: str


class ShowUser(BaseModel):
    username: str

    class Config():
        orm_mode = True

class Login(BaseModel):
    email:str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None
    email: Optional[str] = None


class TodoList(BaseModel):
    code:int
    name:str

    class Config:
        orm_mode = True
    

class CheckList(BaseModel):
    # userid:int
    code:int
    done:bool
    date:datetime.date = datetime.datetime.today().strftime("%Y-%m-%d")

    class Config:
        orm_mode = True