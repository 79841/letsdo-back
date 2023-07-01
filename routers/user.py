from fastapi import APIRouter, Depends, Request
import schemas, database
from sqlalchemy.orm import Session
from repository import user
from fastapi.responses import HTMLResponse


router = APIRouter(
    prefix='/user',
    tags=['users']
)
get_db = database.get_db


@router.post('/', response_model=schemas.ShowUser)
async def create_user(request: schemas.User, db: Session = Depends(get_db)):

    return user.create(request, db)


@router.get('/{username}', response_model=schemas.ShowUser)
async def get_user(username: str, db: Session = Depends(get_db)):
    return user.show(username, db)
