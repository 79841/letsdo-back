from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session

import database
import schemas


from repository import authentication as auth


router = APIRouter(
    prefix='/auth',
    tags=['Authentication']
)


@router.post('/', response_class=Response)
async def sign_in(request: schemas.Login, db_sess: Session = Depends(database.get_db)):
    return auth.sign_in(request, db_sess)


@router.get("/logout")
async def logout() -> Response:
    return auth.logout()
