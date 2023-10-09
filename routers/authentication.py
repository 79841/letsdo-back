from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session

import database
import oauth2
import schemas


from repository import authentication as auth


router = APIRouter(
    prefix='/auth',
    tags=['Authentication']
)


@router.post('/', response_class=Response)
async def sign_in(request: schemas.Login, db_sess: Session = Depends(database.get_db)):
    return auth.sign_in(request, db_sess)


@router.get('/token', response_class=Response)
async def sign_in_by_token(current_user: schemas.User = Depends(oauth2.get_current_user)):
    return auth.sign_in_with_token(current_user)


@router.get("/logout")
async def logout() -> Response:
    return auth.logout()
