from fastapi import APIRouter, Depends, Request, status
import schemas, database, oauth2
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse, JSONResponse, Response, RedirectResponse
from repository import authentication as auth


router = APIRouter(
    prefix='/auth',
    tags=['Authentication']
)


@router.post('/', response_class=Response)
async def signin(request: schemas.Login, db: Session = Depends(database.get_db)):
    return auth.signin(request, db)


@router.get("/logout")
async def logout():
    return auth.logout()
