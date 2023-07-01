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

get_db = database.get_db

def get(db: Session=Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    chatroom = db.query(Participant.chatroom_id).filter(Participant.user_id == current_user.id).first()
    return chatroom

def create(messageTo:int, db: Session=Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):

    messageTo = messageTo if current_user.role == 1 else db.query(User.id).filter_by(role=1)
    chatroom = Chatroom()
    sender = Participant(user_id=current_user.id, chatroom=chatroom)
    reciver = Participant(user_id=messageTo, chatroom=chatroom)
    db.add_all([chatroom, sender, reciver])
    db.commit()
    return chatroom
