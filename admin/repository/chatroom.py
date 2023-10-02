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

from utils.checkAdmin import check_admin


def get_all_chatroom(db: Session, current_user: schemas.User):
    check_admin(db, current_user)
    chatrooms = db.query(Participant.chatroom_id, Participant.user_id).filter(
        Participant.user_id != current_user.id).all()
    return chatrooms
