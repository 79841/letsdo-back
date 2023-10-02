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
from repository import chatroom


router = APIRouter(
    prefix='/chatroom',
    tags=['chatroom']
)
get_db = database.get_db


@router.get("/")
async def get_chatroom(db_sess: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return chatroom.get(db_sess, current_user)


@router.post("/", response_model=schemas.ResponseChatRoom)
async def create_chatroom_with_counselor(db_sess: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):

    return chatroom.create(1, db_sess, current_user)


@router.post("/{message_to}")
async def create_chatroom(message_to: int, db_sess: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):

    return chatroom.create(message_to, db_sess, current_user)

@router.get("/opponent/{chatroom_id}")
async def get_opponent(chatroom_id:int, db_sess:Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return chatroom.get_opponent(chatroom_id, db_sess, current_user)