from sqlalchemy.orm import Session
import models
import schemas
import hashing
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import RedirectResponse, Response, JSONResponse
import datetime
from utils.checkAdmin import check_admin

def create(request: schemas.User, db: Session):

    if db.query(models.User).filter(models.User.role == 1).first():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"관리자가 이미 존재합니다.")

    if db.query(User).filter(User.email == request.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="해당 이메일이 이미 존재합니다.")

    if db.query(User).filter(User.name == request.username).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="해당 이름이 이미 존재합니다.")

    user = dict(request)
    user.update(password=hashing.Hash.bcrypt(user['password']))

    new_user = models.User(**dict(user), role=1)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return JSONResponse(
        jsonable_encoder({"username": user['username']}), status_code=status.HTTP_201_CREATED)

def get_clients(db: Session, current_user: schemas.User):
    # if not check_admin(db, current_user):
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                         detail=f"Please log in as administrator")
    check_admin(db, current_user)
    clients = db.query(models.User).filter(
        models.User.role == 0).all()
    if not clients:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the id '{id}' is not found")
    return clients


def update(request: schemas.UpdateUser, db: Session, current_user: schemas.User):
    user = db.get(models.User, (current_user.id))
    for key, value in dict(request).items():
        if not value:
            continue
        if key == "password":
            setattr(user, key, hashing.Hash.bcrypt(value))
        else:
            setattr(user, key, value)

    db.add(user)
    db.commit()
    return {"msg": "update success"}
