from fastapi import Depends, status, HTTPException, Response
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import schemas
import database
import models
import getToken

from hashing import Hash


def sign_in(request: schemas.Login, db_sess: Session = Depends(database.get_db)) -> JSONResponse:
    user = db_sess.query(models.User).filter(
        models.User.email == request.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Invalid Credentials")

    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Incorrect password")

    access_token = getToken.create_access_token(
        data={"id": user.id, "email": user.email, "username": user.username, "role": user.role})

    response = JSONResponse(
        content={"Authorization": f"Bearer {access_token}"}, status_code=200)
    response.set_cookie(
        "Authorization",
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=1800,
        expires=1800,
    )

    return response


def sign_in_with_token(current_user: schemas.User) -> JSONResponse:
    access_token = getToken.create_access_token(
        data={"id": current_user.id})
    response = JSONResponse(
        content={"Authorization": f"Bearer {access_token}"}, status_code=200)
    response.set_cookie(
        "Authorization",
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=1800,
        expires=1800,
    )

    return response


def logout() -> Response:
    response = Response()
    response.delete_cookie("Authorization")
    return response
