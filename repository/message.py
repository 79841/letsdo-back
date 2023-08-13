import asyncio
import json
from operator import and_
from typing import Optional
import aioredis
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
import aioredis
import asyncio


# datetime_utc = datetime.utcnow()

timezone_kst = timezone(timedelta(hours=9))

connected_chat_clients = {}
connected_message_check_clients = {}


async def get_redis_client():
    return await aioredis.from_url("redis://localhost")

    # async for message in channel.iter():
    # data = json.loads(message)
    # print(message)
    # await asyncio.gather(*[client.send_json(data) for client in connected_clients])


async def service_unread_message_count(websocket: WebSocket, chatroom_id: int, db: Session, current_user: schemas.User):

    async def subscribe_channel():
        redis = await get_redis_client()
        p = redis.pubsub()
        await p.subscribe(f"new_message")

        while True:
            message = await p.get_message()
            if message and "data" in message and isinstance(message["data"], bytes):
                data = json.loads(message["data"].decode("utf-8"))
                if "content" in data:
                    unread_message_count = get_unread_message_count(
                        chatroom_id, db, current_user)
                    websocket.send_text(json.dumps(unread_message_count))

    await websocket.accept()
    connected_message_check_clients.update({current_user.id: websocket})

    unread_message_count = await get_unread_message_count(
        chatroom_id, db, current_user)

    await websocket.send_text(json.dumps(unread_message_count))

    try:
        await subscribe_channel()
    except Exception as e:
        print("WebSocket error:", e)
    finally:
        connected_message_check_clients.pop(current_user.id)


async def get(chatroomId: int, db: Session = Depends(get_db)):
    messages = db.query(Message).filter(
        Message.chatroom_id == chatroomId).all()
    messages = [{"id": message.id, "content": message.content, "userId": message.user_id, "timestamp": message.timestamp,
                 "messageFrom": message.user.username, "chatroomId": message.chatroom.id} for message in messages]
    return messages


async def update_last_read_message(chatroom_id: int, message_id: int, db: Session, current_user: schemas.User):
    participant = db.query(Participant).filter(and_(
        Participant.chatroom_id == chatroom_id, Participant.user_id == current_user.id)).first()
    participant.last_read_message_id = message_id
    db.commit()
    return {"message": "update last read message success"}


async def get_unread_message_count(chatroom_id: int, db: Session, current_user: schemas.User):

    last_read_message_id, = db.query(Participant.last_read_message_id).filter(and_(
        Participant.chatroom_id == chatroom_id, Participant.user_id == current_user.id)).first()

    unread_message_count = db.query(Message).filter(and_(
        Message.chatroom_id == chatroom_id, Message.id > last_read_message_id)).count()

    return unread_message_count


async def create_message(request: schemas.RequestCreateMessage, chatroom_id: int, db: Session, current_user: schemas.User):
    message = Message(
        content=request.content, timestamp=datetime.now(), user_id=current_user.id, chatroom_id=chatroom_id)

    db.add(message)
    db.commit()

    redis = await get_redis_client()
    await redis.publish(f"new_message",
                        json.dumps({"content": request.content}))
    return {"message": "Message created"}


async def chat(websocket: WebSocket, chatroomId: Optional[int] = None, token: Optional[str] = None, messageTo: Optional[int] = None, db: Session = Depends(get_db)):
    await websocket.accept()

    current_user = oauth2.get_current_user(token.split()[1])
    connected_chat_clients.update({current_user.id: websocket})

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

            participant = db.query(Participant).filter(and_(
                Participant.chatroom_id == chatroom.id, Participant.user_id == current_user.id)).first()

            participant.last_read_message_id = message.id

            db.commit()

            for participant in [messageTo, current_user.id]:
                if participant in connected_chat_clients:
                    message = {"id": message.id, "content": content, "userId": current_user.id, "messageFrom": current_user.username,
                               "chatroomId": chatroom.id, "timestamp": message.timestamp.strftime('%Y-%m-%d %H:%M:%S')}
                    await connected_chat_clients[participant].send_text(json.dumps(message))

    except WebSocketDisconnect:
        print(connected_chat_clients)
        connected_chat_clients.pop(current_user.id)
