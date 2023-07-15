from fastapi import APIRouter, Depends, Request
import hashing
from models import User
import oauth2
import schemas
import database
from sqlalchemy.orm import Session
from repository import user
from fastapi.responses import HTMLResponse


router = APIRouter(
    prefix='/user',
    tags=['users']
)
get_db = database.get_db


@router.post('/', response_model=schemas.ShowUser)
async def createUser(request: schemas.User, db: Session = Depends(get_db)):
    return user.create(request, db)


@router.get('/{username}', response_model=schemas.ShowUser)
async def getUser(username: str, db: Session = Depends(get_db)):
    return user.show(username, db)


@router.patch("/")
async def updateUser(request: schemas.UpdateUser, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return user.update(request, db, current_user)
