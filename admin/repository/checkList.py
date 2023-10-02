from sqlalchemy.orm import Session
import oauth2
import schemas
import hashing
from models import CheckList
from fastapi import Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import RedirectResponse, Response, JSONResponse
import datetime

from utils.checkAdmin import check_admin


def create(request: list[schemas.CheckList], db: Session, current_user: schemas.User = Depends(oauth2.get_current_user)):

    for check in request:
        dbCheck = db.get(CheckList, (current_user.id, check.code, check.date))

        if dbCheck:

            for key, value in dict(check).items():
                setattr(dbCheck, key, value)
        else:

            check = dict(check)
            check.update({"user_id": current_user.id})
            dbCheck = CheckList(**check)

            db.add(dbCheck)

        db.commit()

    return JSONResponse(
        jsonable_encoder(request), status_code=status.HTTP_201_CREATED)


def get_by_date(user_id: int, date: str, db: Session, current_user: schemas.User = Depends(oauth2.get_current_user)):
    check_admin(db, current_user)
    checkList = db.query(CheckList.date, CheckList.code, CheckList.done).filter(CheckList.date == date).\
        filter(CheckList.user_id == user_id).all()

    return checkList


def getAll(db: Session):
    checkList = db.query(CheckList).all()
    if not checkList:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"There is nothing to do.")
    return checkList


def delete(code: int, db: Session):
    checkList = db.query(CheckList).filter(CheckList.code == code).delete()
    db.commit()
    return checkList


def get_by_period(user_id: int, start_date: str, end_date: str, db: Session, current_user: schemas.User = Depends(oauth2.get_current_user)):
    check_admin(db, current_user)
    checkList = db.query(CheckList.code, CheckList.date, CheckList.done).filter(user_id == CheckList.user_id).filter(
        CheckList.date >= start_date, CheckList.date <= end_date).all()

    return checkList
