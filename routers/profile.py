from fastapi import APIRouter, Depends
import oauth2
import schemas
import database
from sqlalchemy.orm import Session
from fastapi import UploadFile, File
from repository import profile

router = APIRouter(
    prefix='/profile',
    tags=['profile']
)
get_db = database.get_db


@router.post("/")
def uploadProfileImage(file: UploadFile = File(...), db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return profile.create(file, db, current_user)


@router.get("/")
def getProfileImage(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return profile.get(db, current_user)


@router.patch("/")
def updateProfileImage(file: UploadFile = File(...), db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return profile.update(file, db, current_user)


@router.delete("/")
def deleteProfileImage(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return profile.delete(db, current_user)
