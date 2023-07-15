import datetime
from fastapi import APIRouter, Depends, Request
import oauth2
import schemas
import database
from sqlalchemy.orm import Session
from repository import checkList
from fastapi.responses import HTMLResponse
from typing import List
from datetime import datetime, timedelta, timezone

router = APIRouter(
    prefix='/checklist',
    tags=['checklist']
)
get_db = database.get_db

todayDate = datetime.today().astimezone(
    timezone(timedelta(hours=9))).strftime("%Y-%m-%d")


@router.post('/', response_model=schemas.CheckList)
async def createCheckList(request: list[schemas.CheckList], db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return checkList.create(request, db, current_user)


@router.get('/', response_model=list[schemas.ResponseCheckList])
@router.get('/date/{date}', response_model=list[schemas.ResponseCheckList])
async def getCheckList(date: str = todayDate, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return checkList.getByDate(date, db, current_user)


@router.get('/dates', response_model=list[schemas.ResponseCheckList])
async def getCheckList(start_date: str = todayDate, end_date: str = todayDate, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return checkList.getByPeriod(start_date, end_date, db, current_user)


@router.delete('/{code}')
async def deleteTodo(code: int, db: Session = Depends(get_db)):
    return checkList.delete(code, db)
