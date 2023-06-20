from sqlalchemy.orm import Session
import models, schemas, hashing
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
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the username '{username}' is not found")

    return user
