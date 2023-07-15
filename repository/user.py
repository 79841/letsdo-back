from sqlalchemy.orm import Session
import models
import schemas
import hashing
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import RedirectResponse, Response, JSONResponse
import datetime


def create(request: schemas.User, db: Session):

    user = dict(request)
    user.update(password=hashing.Hash.bcrypt(user['password']))

    new_user = models.User(**dict(user))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return JSONResponse(
        jsonable_encoder({"username": user['username']}), status_code=status.HTTP_201_CREATED)


def show(username: str, db: Session):
    user = db.query(models.User).filter(
        models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the username '{username}' is not found")

    return user


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

    return user
