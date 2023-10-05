# from ctypes import WinError
from datetime import date, datetime, timezone, timedelta

from typing import List, Optional
from fastapi import Form
from pydantic import BaseModel
from sqlalchemy import Date


class User(BaseModel):
    id: int
    email: str
    username: str
    password: str
    role: int = 0


class UpdateUser(BaseModel):
    email: Optional[str]
    username: Optional[str]
    password: Optional[str]


class CreateUser(BaseModel):
    email: str
    username: str
    password: str


class ShowUser(BaseModel):
    id: int
    email: str
    username: str

    class Config():
        from_attributes = True


class Login(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None
    email: Optional[str] = None
    username: Optional[str] = None
    role: Optional[int] = None


class TodoList(BaseModel):
    code: int
    name: str

    class Config:
        from_attributes = True


class CheckList(BaseModel):
    # userid:int
    code: int
    done: bool
    date: Optional[date]

    class Config:
        from_attributes = True


class ResponseCheckList(BaseModel):
    date: date
    code: int
    done: bool


class ResponseChatRoom(BaseModel):
    id: int


class RequestCreateMessage(BaseModel):
    content: str


# class ResponseMessage(BaseModel):
#     id:int
#     content:str
#     user_id:int
#     chatroom_id:int
#     timestamp:datetime.datetime

#     class config:
#         orm_mode = True
