from models import User
from sqlalchemy import and_
import schemas
from sqlalchemy.orm import Session
from fastapi import HTTPException, status


def check_admin(db: Session, current_user: schemas.User):
    admin = db.query(User).filter(current_user.id == User.id).first()
    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"사용자가 존재하지 않습니다.")
    if not admin.role:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"관리자 권한이 없습니다.")
    return
