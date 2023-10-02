# import datetime
# import json
from fastapi import APIRouter, Depends, Request
# from sqlalchemy import or_
# from getToken import verify_token
# from models import Chatroom, Message, Participant, User
from sqlalchemy.orm import Session
import oauth2
# from repository.message import chat
import schemas
import database

# from repository import checkList
# from fastapi.responses import HTMLResponse
# from typing import List, Optional
# from fastapi.security import APIKeyHeader
# from starlette.requests import Request as WebsocRequest
# from fastapi.security import APIKeyQuery
# from fastapi_jwt_auth import AuthJWT
from admin.repository import chatroom


router = APIRouter(
    prefix='/admin/chatroom',
    tags=['(ADMIN) chatroom']
)
get_db = database.get_db


@router.get("/")
async def get_all_chatroom(db_sess: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return chatroom.get_all_chatroom(db_sess, current_user)
