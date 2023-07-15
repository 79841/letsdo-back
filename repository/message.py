import json
from typing import Optional
from sqlalchemy.orm import Session
from database import get_db
import oauth2
import schemas
import hashing
from models import Chatroom, CheckList, Message, Participant, User
from fastapi import Depends, HTTPException, WebSocket, WebSocketDisconnect, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import RedirectResponse, Response, JSONResponse
from datetime import datetime, timezone, timedelta


# datetime_utc = datetime.utcnow()

timezone_kst = timezone(timedelta(hours=9))

connectedClients = {}


async def get(chatroomId: int, db: Session = Depends(get_db)):
    messages = db.query(Message).filter(
        Message.chatroom_id == chatroomId).all()
    messages = [{"content": message.content, "userId": message.user_id, "timestamp": message.timestamp,
                 "messageFrom": message.user.username, "chatroomId": message.chatroom.id} for message in messages]
    return messages


async def chat(websocket: WebSocket, chatroomId: Optional[int] = None, token: Optional[str] = None, messageTo: Optional[int] = None, db: Session = Depends(get_db)):
    await websocket.accept()

    current_user = oauth2.get_current_user(token.split()[1])
    connectedClients.update({current_user.id: websocket})

    chatroom = db.query(Chatroom).filter_by(id=chatroomId).first()
    messageTo = messageTo if current_user.role == 1 else db.query(
        User.id).filter_by(role=1)

    try:
        while True:
            content = await websocket.receive_text()

            message = Message(
                content=content, timestamp=datetime.now(), user_id=current_user.id, chatroom=chatroom)
            db.add(message)
            db.commit()
            for participant in [messageTo, current_user.id]:
                if participant in connectedClients:
                    message = {"content": content, "userId": current_user.id, "messageFrom": current_user.username,
                               "chatroomId": chatroom.id, "timestamp": message.timestamp.strftime('%Y-%m-%d %H:%M:%S')}
                    await connectedClients[participant].send_text(json.dumps(message))

    except WebSocketDisconnect:
        connectedClients.pop(websocket)
