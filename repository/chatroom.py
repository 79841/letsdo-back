import datetime
import json
from fastapi import APIRouter, Depends, Query, Request, WebSocket, WebSocketDisconnect
from sqlalchemy import or_
from getToken import verify_token
from models import Chatroom, Message, Participant, User
import oauth2
from repository.message import chat
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
from sqlalchemy import and_

get_db = database.get_db


def get(db: Session, current_user: schemas.User ):
    chatroom = db.query(Participant.chatroom_id).filter(
        Participant.user_id == current_user.id).first()
    return chatroom


def create(messageTo: int, db: Session, current_user: schemas.User ):

    messageTo = messageTo if current_user.role == 1 else db.query(
        User.id).filter_by(role=1)
    chatroom = Chatroom()
    sender = Participant(user_id=current_user.id, chatroom=chatroom)
    reciver = Participant(user_id=messageTo, chatroom=chatroom)
    db.add_all([chatroom, sender, reciver])
    db.commit()
    return schemas.ResponseChatRoom(id=chatroom.id)

def get_opponent(chatroom_id:int, db:Session, current_user: schemas.User):
    opponent = db.query(Participant.user_id).filter(and_(Participant.chatroom_id == chatroom_id, Participant.user_id != current_user.id)).first()
    return opponent