from sqlalchemy.orm import Session
from models import User
import schemas
import hashing
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import RedirectResponse, Response, JSONResponse
import datetime



def create(request: schemas.User, db: Session):

    if db.query(User).filter(User.email == request.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="해당 이메일이 이미 존재합니다.")

    if db.query(User).filter(User.name == request.username).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="해당 이름이 이미 존재합니다.")

    user = dict(request)
    user.update(password=hashing.Hash.bcrypt(user['password']))

    new_user = User(**dict(user))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return JSONResponse(
        jsonable_encoder({"username": user['username']}), status_code=status.HTTP_201_CREATED)


def show(db: Session, current_user:schemas.User):
    user = db.query(User).filter(
        User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the id '{id}' is not found")
    return user


def update(request: schemas.UpdateUser, db: Session, current_user: schemas.User):
    user = db.get(User, (current_user.id))
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
