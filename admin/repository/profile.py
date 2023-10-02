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


def get(db: Session, current_user: schemas.User, user_id: Optional[int] = None):
    profile = db.query(Profile).filter(
        Profile.user_id == user_id).first() if user_id else db.query(Profile).filter(
        Profile.user_id == current_user.id).first()
    if not profile or not profile.path:
        raise HTTPException(status_code=404, detail="Profile image not found")

    return FileResponse(profile.path)
