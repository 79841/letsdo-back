import asyncio
import json
from operator import and_
from typing import Optional
import aioredis
from fastapi.websockets import WebSocketState
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
from sqlalchemy import func, select

from utils.checkAdmin import check_admin

datetime_utc = datetime.utcnow()

timezone_kst = timezone(timedelta(hours=9))

connected_messages_check_clients = {}


async def get_redis_client():
    return await aioredis.from_url("redis://localhost")


async def get_all_unread_message_count_on_async_session(db: Session, current_user: schemas.User):

    stmt = (
        select([Message.chatroom_id, func.count().label('unread_message_count')])
        .select_from(Message)
        .join(Participant, Participant.chatroom_id == Message.chatroom_id)
        .where(Participant.user_id == current_user.id)
        .where(Participant.last_read_message_id < Message.id)
        .group_by(Message.chatroom_id)
    )
    result = await db.execute(stmt)
    unread_message_counts = [{"chatroom_id": row[0],
                              "unread_message_count": row[1]} for row in result]
    return unread_message_counts


async def get_all_last_messages_on_async_session(db: Session, current_user: schemas.User):

    subquery = (
        select([func.max(Message.id).label('id')])
        .join(Participant, Message.chatroom_id == Participant.chatroom_id)
        .filter(Participant.user_id == current_user.id)
        .group_by(Message.chatroom_id)
        .alias('m2')
    )

    stmt = (
        select(Message)
        .join(subquery, Message.id == subquery.c.id)
    )

    result = await db.execute(stmt)
    last_messages = result
    message_dicts = [dict(id=row.Message.id, content=row.Message.content, user_id=row.Message.user_id,
                          chatroom_id=row.Message.chatroom_id, timestamp=row.Message.timestamp.strftime('%Y-%m-%d %H:%M:%S')) for row in last_messages]

    return message_dicts


async def service_all_unread_message_count(websocket: WebSocket, db: Session, current_user: schemas.User):

    check_admin(db, current_user)
    try:
        if (current_user.id in connected_messages_check_clients):
            await connected_messages_check_clients[current_user.id].close()
        await websocket.accept()
        connected_messages_check_clients[current_user.id] = websocket

        unread_messages_count = get_all_unread_message_count(db, current_user)
        last_messages = get_all_last_messages(db, current_user)
        db.close()

        await websocket.send_text(json.dumps([unread_messages_count, last_messages]))
    except WebSocketDisconnect as e:
        if current_user.id in connected_messages_check_clients:
            connected_messages_check_clients.pop(current_user.id)
        await websocket.close()

    async def subscribe_channel():
        x = 0
        redis = await get_redis_client()
        p = redis.pubsub()
        await p.subscribe(f"new_message")

        while websocket.application_state == WebSocketState.CONNECTED:

            try:
                message = await p.get_message()
                if message and "data" in message and isinstance(message["data"], bytes):
                    data = json.loads(message["data"].decode("utf-8"))
                    if "content" in data:
                        async for session in get_async_session():
                            async with session.begin():
                                unread_all_message_count = await get_all_unread_message_count_on_async_session(
                                    session, current_user)
                                last_messages = await get_all_last_messages_on_async_session(
                                    session, current_user)
                                await websocket.send_text(json.dumps([unread_all_message_count, last_messages]))

            except WebSocketDisconnect:
                print("WebSocket disconnected")
                break
            except Exception as e:
                print("WebSocket error:", e)
                break

            await asyncio.sleep(1)
        await p.close()
    try:
        await subscribe_channel()
    except WebSocketDisconnect as e:
        if current_user.id in connected_messages_check_clients:
            connected_messages_check_clients.pop(current_user.id)
        await websocket.close()
    except Exception as e:
        print("WebSocket error:", e)

    finally:
        if current_user.id in connected_messages_check_clients:
            connected_messages_check_clients.pop(current_user.id)


def get_all_unread_message_count(db: Session, current_user: schemas.User):

    check_admin(db, current_user)
    unread_message_counts = db.query(Message.chatroom_id, func.count(Message.id).label('unread_message_count')).\
        join(Participant, Participant.chatroom_id == Message.chatroom_id).\
        filter(Participant.user_id == current_user.id).\
        filter(Participant.last_read_message_id < Message.id).\
        group_by(Message.chatroom_id).\
        all()

    results_as_dict = [{"chatroom_id": chatroom_id, "unread_message_count": count}
                       for chatroom_id, count in unread_message_counts]

    return results_as_dict


def get_all_last_messages(db: Session, current_user: schemas.User):
    subquery = (
        db.query(func.max(Message.id).label('id'))
        .join(Participant, Message.chatroom_id == Participant.chatroom_id)
        .filter(Participant.user_id == current_user.id)
        .group_by(Message.chatroom_id)
        .subquery()
    )

    stmt = (
        db.query(Message)
        .join(subquery, Message.id == subquery.c.id)
    )

    results = stmt.all()

    message_dicts = [dict(id=row.id, content=row.content, user_id=row.user_id,
                          chatroom_id=row.chatroom_id, timestamp=row.timestamp.strftime('%Y-%m-%d %H:%M:%S')) for row in results]

    return message_dicts
