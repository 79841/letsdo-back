import os
import shutil
from fastapi import HTTPException
from config import settings
from models import Profile
import schemas
from sqlalchemy.orm import Session
from fastapi import UploadFile
import time
from typing import Optional
from fastapi.responses import FileResponse


def create(file: UploadFile, db: Session, current_user: schemas.User):
    profile = db.query(Profile).filter(
        current_user.id == Profile.user_id).first()

    if profile:
        return {"message": "Profile image already existed"}

    profileImageDir = os.path.join(os.getcwd(), settings.PROFILE_IMAGE_DIR)
    fileExtension = os.path.splitext(file.filename)[1]
    filePath = f"{profileImageDir}/{current_user.id}_{round(time.time() * 1000)}{fileExtension}"
    with open(filePath, "wb") as image:
        shutil.copyfileobj(file.file, image)

    newProfile = Profile(user_id=current_user.id, path=filePath)
    db.add(newProfile)
    db.commit()

    return {"message": "Profile image uploaded successfully"}


def get(db: Session, current_user: schemas.User):
    profile = db.query(Profile).filter(
        Profile.user_id == current_user.id).first()
    if not profile or not profile.path:
        raise HTTPException(status_code=404, detail="Profile image not found")

    return FileResponse(profile.path)


def get_by_id(db: Session, user_id: int):
    profile = db.query(Profile).filter(
        Profile.user_id == user_id).first()
    if not profile or not profile.path:
        raise HTTPException(status_code=404, detail="Profile image not found")

    return FileResponse(profile.path)


def update(file: UploadFile, db: Session, current_user: schemas.User):
    profile = db.query(Profile).filter(
        Profile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="User not found")

    if profile.path:
        os.remove(profile.path)

    profileImageDir = os.path.join(os.getcwd(), settings.PROFILE_IMAGE_DIR)
    fileExtension = os.path.splitext(file.filename)[1]
    filePath = f"{profileImageDir}/{current_user.id}_{round(time.time() * 1000)}{fileExtension}"
    with open(filePath, "wb") as image:
        shutil.copyfileobj(file.file, image)

    profile.path = filePath
    db.commit()

    return {"message": "Profile image updated successfully"}


def delete(db: Session, current_user: schemas.User):
    profile = db.query(Profile).filter(
        Profile.user_id == current_user.id).first()
    if not profile or not profile.path:
        raise HTTPException(status_code=404, detail="Profile image not found")

    os.remove(profile.path)
    db.delete(profile)
    db.commit()

    return {"message": "Profile image deleted successfully"}
