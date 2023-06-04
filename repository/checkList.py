from sqlalchemy.orm import Session
import oauth2
import schemas, hashing
from models import CheckList
from fastapi import Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import RedirectResponse, Response, JSONResponse
import datetime


def create(request: list[schemas.CheckList], db: Session, current_user: schemas.User = Depends(oauth2.get_current_user)):

    for check in request:
        dbCheck = db.get(CheckList, (current_user.id, check.code, check.date))

        if dbCheck:

            for key, value in dict(check).items():
                setattr(dbCheck, key, value)
        else:
            
            check = dict(check)
            check.update({"userid":current_user.id})
            dbCheck = CheckList(**check)
            
        db.add(dbCheck)
        db.commit()

    return JSONResponse(
        jsonable_encoder(request), status_code=status.HTTP_201_CREATED)


def getByDate(date:str, db: Session, current_user: schemas.User = Depends(oauth2.get_current_user)):
    checkList = db.query(CheckList).filter(CheckList.date == date).\
                                    filter(CheckList.userid == current_user.id).all()
    return checkList


def getAll(db: Session):
    checkList = db.query(CheckList).all()
    if not checkList:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"There is nothing to do.")
    return checkList

def delete(code:int, db: Session):
    checkList = db.query(CheckList).filter(CheckList.code == code).delete()
    db.commit()
    return checkList