import datetime
from fastapi import APIRouter, Depends, Request
import oauth2
import schemas, database
from sqlalchemy.orm import Session
from repository import checkList
from fastapi.responses import HTMLResponse
from typing import List


router = APIRouter(
    prefix='/checklist',
    tags=['checklist']
)
get_db = database.get_db


@router.post('/', response_model=schemas.CheckList)
async def createCheckList(request: list[schemas.CheckList], db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return checkList.create(request, db, current_user)


@router.get('/', response_model=list[schemas.ResponseCheckList])
@router.get('/{date}', response_model=list[schemas.ResponseCheckList])
async def getCheckList(date:str=datetime.datetime.today().strftime("%Y-%m-%d"), db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return checkList.getByDate(date, db, current_user)


@router.delete('/{code}')
async def deleteTodo(code:int, db:Session = Depends(get_db)):
    return checkList.delete(code, db)
