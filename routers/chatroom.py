import datetime
import json
from fastapi import APIRouter, Depends, Query, Request, WebSocket, WebSocketDisconnect
from sqlalchemy import or_
from getToken import verify_token
from models import Chatroom, Message, Participant, User
import oauth2
from repository.message import chat
import schemas, database
from sqlalchemy.orm import Session
from repository import checkList
from fastapi.responses import HTMLResponse
from typing import List, Optional
from fastapi.security import APIKeyHeader
from starlette.requests import Request as WebsocRequest
from fastapi.security import APIKeyQuery
from fastapi_jwt_auth import AuthJWT
from repository import chatroom


router = APIRouter(
    prefix='/chatroom',
    tags=['chatroom']
)
get_db = database.get_db

@router.get("/")
async def getChatroom(request:Request, db: Session=Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return chatroom.get(db, current_user)

@router.post("/")
async def createChatroom(request:Request, db: Session=Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):

    return chatroom.create(1, db, current_user)


@router.post("/{messageTo}")
async def createChatroom(request:Request, messageTo:int, db: Session=Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):

    return chatroom.create(messageTo, db, current_user)