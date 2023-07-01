from sqlalchemy.orm import Session
import models, schemas, hashing
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import RedirectResponse, Response, JSONResponse
import datetime


def create(request: schemas.TodoList, db: Session):

    todo = models.TodoList(**dict(request))
    db.add(todo)
    db.commit()
    db.refresh(todo)
    
    return JSONResponse(
        jsonable_encoder({"todo": dict(request)['name']}), status_code=status.HTTP_201_CREATED)


def getAll(db: Session):
    todoList = db.query(models.TodoList).all()
    if not todoList:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"There is nothing to do.")
    return todoList

def delete(code:int, db: Session):
    todoList = db.query(models.TodoList).filter(models.TodoList.code == code).delete()
    db.commit()
    return todoList