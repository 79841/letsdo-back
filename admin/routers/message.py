import datetime
import json
from fastapi import APIRouter, Depends, Query, Request, WebSocket, WebSocketDisconnect
from sqlalchemy import or_
from getToken import verify_token
from models import Chatroom, Message, Participant, User
import oauth2
from admin.repository import message
import schemas
import database
from sqlalchemy.orm import Session
from repository import checkList
from fastapi.responses import HTMLResponse
from typing import List, Optional
from fastapi.security import APIKeyHeader
from starlette.requests import Request as WebsocRequest

from fastapi.security import APIKeyQuery
from fastapi_jwt_auth import AuthJWT


router = APIRouter(
    prefix='/admin/message',
    tags=['(ADMIN) message']
)
get_db = database.get_db

connectedClients = {}


# @router.get("/")
# async def getOpponents(db: Session, current_user: schemas.User = Depends(oauth2.get_current_user)):


# @router.get("/{chatroom_id}")
# async def getMessages(chatroom_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
#     return await message.get(chatroom_id, db)


# @router.patch("/last/read/{chatroom_id}")
# async def update_last_read_message(chatroom_id: int, message_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
#     return await message.update_last_read_message(chatroom_id, message_id, db, current_user)


@router.get("/unread/count/all/")
async def get_all_unread_message_count(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return await message.get_all_unread_message_count(db, current_user)


# @router.post("/create/{chatroom_id}")
# async def create_message(request: schemas.RequestCreateMessage, chatroom_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
#     return await message.create_message(request, chatroom_id, db, current_user)


# @router.websocket("/ws/")
# @router.websocket("/ws/{chatroom_id}")
# async def websocketEndpoint(websocket: WebSocket, chatroom_id: Optional[int] = None, token: Optional[str] = None, message_to: Optional[int] = None, db: Session = Depends(get_db)):
#     await message.chat(websocket, chatroom_id, token, message_to, db)


@router.websocket("/unread/count/all/ws/")
async def service_unread_message_count(websocket: WebSocket, token: str, db: Session = Depends(get_db)):
    current_user = oauth2.get_websocket_user(token)
    await message.service_all_unread_message_count(websocket, db, current_user)
