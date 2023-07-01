import datetime
import json
from fastapi import APIRouter, Depends, Query, Request, WebSocket, WebSocketDisconnect
from sqlalchemy import or_
from getToken import verify_token
from models import Chatroom, Message, Participant, User
import oauth2
from repository import message
import schemas, database
from sqlalchemy.orm import Session
from repository import checkList
from fastapi.responses import HTMLResponse
from typing import List, Optional
from fastapi.security import APIKeyHeader
from starlette.requests import Request as WebsocRequest

from fastapi.security import APIKeyQuery
from fastapi_jwt_auth import AuthJWT


router = APIRouter(
    prefix='/message',
    tags=['message']
)
get_db = database.get_db

connectedClients = {}


# @router.get("/")
# async def getOpponents(db: Session, current_user: schemas.User = Depends(oauth2.get_current_user)):


@router.get("/{chatroomId}")
async def getMessages(chatroomId:int, db: Session=Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):

    return await message.get(chatroomId, db)


@router.websocket("/ws/")
@router.websocket("/ws/{chatroomId}")
async def websocketEndpoint(websocket: WebSocket, chatroomId:Optional[int]=None, token:Optional[str]=None, message_to:Optional[int]=None, db:Session=Depends(get_db)):
    await message.chat(websocket, chatroomId, token, message_to, db)
