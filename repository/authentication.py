from fastapi import Depends, Request, status, HTTPException, Response
import schemas, database, models, getToken
from sqlalchemy.orm import Session
from hashing import Hash
from fastapi.responses import  JSONResponse, RedirectResponse


def signin(request: schemas.Login, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(
        models.User.email == request.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Credentials")

    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect password")

    access_token = getToken.create_access_token(
        data={"id": user.id, "email": user.email, "username":user.username, "role":user.role})

    response = JSONResponse(content={"Authorization":f"Bearer {access_token}"}, status_code=200)
    response.set_cookie(
        "Authorization",
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=1800,
        expires=1800,
        
    )

    return response


def logout():
    response = Response()
    response.delete_cookie("Authorization")
    return response
