import datetime
import json
from fastapi import APIRouter, Depends, Request, WebSocket, WebSocketDisconnect
from sqlalchemy import or_
from models import Message, User
import oauth2
import schemas, database
from sqlalchemy.orm import Session
from repository import checkList
from fastapi.responses import HTMLResponse
from typing import List


router = APIRouter(
    prefix='/message',
    tags=['message']
)
get_db = database.get_db

connected_clients = {}


# @router.get("/")
# async def getOpponents(db: Session, current_user: schemas.User = Depends(oauth2.get_current_user)):

    

@router.get("/{messageTo}", response_model=list[schemas.ResponseMessage])
async def getMessages(messageTo:int, db: Session, current_user: schemas.User = Depends(oauth2.get_current_user)):
    messages = db.query(Message).\
        filter(or_(Message.message_from == current_user.id, Message.message_to == current_user.id)).\
        filter(or_(Message.message_from == messageTo, Message.message_to == messageTo))
    

@router.websocket("/ws/")
@router.websocket("/ws/{messageTo}")
async def websocketEndpoint(websocket: WebSocket, messageTo:int, db: Session, current_user: schemas.User = Depends(oauth2.get_current_user)):
    await websocket.accept()
    connected_clients.update({current_user.id:websocket})

    if current_user.role == 0:
        messageTo = db.query(User.id).filter(User.role == 1).first()

    try:
        while True:
            content = await websocket.receive_text()
            newMessage = Message({"message_to":messageTo, "message_from":current_user.id, "content":content})
            db.add(newMessage)
            db.commit()
            db.refresh(newMessage)

            sendMessage(messageTo, current_user.id, content)

    except WebSocketDisconnect:
        connected_clients.pop(websocket)

async def sendMessage(messageTo:int, messageFrom:int,content:str):
    try:
        message = {"content":content, "messageTo":messageTo, "messageFrom":messageFrom}
        await connected_clients[messageTo].send_text(json.encoder(message))
    except:
        ...