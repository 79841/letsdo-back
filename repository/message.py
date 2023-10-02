import asyncio
import json
from operator import and_
from typing import Optional
import aioredis
from sqlalchemy.orm import Session
from database import AsyncSessionLocal, get_async_session, get_db
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
from database import async_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select
from sqlalchemy import func

# datetime_utc = datetime.utcnow()

timezone_kst = timezone(timedelta(hours=9))

connected_chat_clients = {}
connected_message_check_clients = {}


async def get_redis_client():
    return await aioredis.from_url("redis://localhost")


async def get_unread_message_count_on_async_session(chatroom_id: int, db: Session, current_user: schemas.User):

    stmt = select(Participant.last_read_message_id).where(
        Participant.chatroom_id == chatroom_id).where(Participant.user_id == current_user.id)
    result = await db.execute(stmt)
    last_read_message_id = result.scalar()

    stmt = select(func.count()).where(Message.chatroom_id == chatroom_id).where(
        Message.id > last_read_message_id)
    result = await db.execute(stmt)
    unread_message_count = result.scalar()
    return unread_message_count


async def service_unread_message_count(websocket: WebSocket, chatroom_id: int, db: Session, current_user: schemas.User):

    # # async_session_instance = AsyncSession(async_engine)
    # if (current_user.id in connected_message_check_clients):
    #     await connected_message_check_clients[current_user.id].close()

    async def subscribe_channel():
        redis = await get_redis_client()
        p = redis.pubsub()
        await p.subscribe(f"new_message")

        while True:
            message = await p.get_message()
            if message and "data" in message and isinstance(message["data"], bytes):
                print(message)
                data = json.loads(message["data"].decode("utf-8"))
                if "content" in data:

                    # async with AsyncSessionLocal() as session:
                    #     unread_message_count = await get_unread_message_count_on_async_session(
                    #         chatroom_id, session, current_user)
                    #     await websocket.send_text(json.dumps(unread_message_count))

                    async for session in get_async_session():
                        async with session.begin():
                            unread_message_count = await get_unread_message_count_on_async_session(
                                chatroom_id, session, current_user)
                            await websocket.send_text(json.dumps(unread_message_count))
            await asyncio.sleep(1)

    await websocket.accept()
    connected_message_check_clients.update({current_user.id: websocket})

    unread_message_count = await get_unread_message_count(
        chatroom_id, db, current_user)

    # print(unread_message_count)

    await websocket.send_text(json.dumps(unread_message_count))

    try:
        await subscribe_channel()
    except Exception as e:
        print("WebSocket error:", e)
    finally:
        if current_user.id in connected_message_check_clients:
            connected_message_check_clients.pop(current_user.id)
        await websocket.close()


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

    unread_message_count = db.query(Message).populate_existing().filter(and_(
        Message.chatroom_id == chatroom_id, Message.id > last_read_message_id)).count()
    return unread_message_count


async def create_message(request: schemas.RequestCreateMessage, chatroom_id: int, db: Session, current_user: schemas.User):
    message = Message(
        content=request.content, timestamp=datetime.now(), user_id=current_user.id, chatroom_id=chatroom_id)

    db.add(message)
    db.commit()
    db.close()
    print("new message")
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

    print("service start")

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

            redis = await get_redis_client()
            await redis.publish(f"new_message", json.dumps({"content": content}))

    except WebSocketDisconnect as e:
        print(e)
        await close_websocket(current_user.id)
    finally:
        db.close()

    print("service end")
    # if current_user.id in connected_chat_clients:
    #     connected_chat_clients.pop(current_user.id)


async def close_websocket(user_id: int):
    websocket = connected_chat_clients.get(user_id)
    if websocket:
        # await websocket.close()
        del connected_chat_clients[user_id]
