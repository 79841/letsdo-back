from fastapi import APIRouter, Depends
import oauth2
import schemas
import database
from sqlalchemy.orm import Session
from fastapi import UploadFile, File
from repository import profile
from typing import Optional

router = APIRouter(
    prefix='/admin/profile',
    tags=['(ADMIN) profile']
)
get_db = database.get_db


@router.get("/all")
def getProfileImage(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return profile.get(db, current_user)
