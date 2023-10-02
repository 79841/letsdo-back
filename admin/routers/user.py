from fastapi import APIRouter, Depends, Request
import hashing
from models import User
import oauth2
import schemas
import database
from sqlalchemy.orm import Session
from admin.repository import user
from fastapi.responses import HTMLResponse
from typing import List

router = APIRouter(
    prefix='/admin',
    tags=['(ADMIN) users']
)

get_db = database.get_db


@router.get("/all/clients", response_model=List[schemas.ShowUser])
async def get_clients(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return user.get_clients(db, current_user)
