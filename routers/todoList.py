from fastapi import APIRouter, Depends, Request
import schemas, database
from sqlalchemy.orm import Session
from repository import todoList
from fastapi.responses import HTMLResponse
from typing import List


router = APIRouter(
    prefix='/todolist',
    tags=['todo']
)
get_db = database.get_db


@router.post('/', response_model=schemas.TodoList)
async def createTodo(request: schemas.TodoList, db: Session = Depends(get_db)):
    return todoList.create(request, db)


@router.get('/', response_model=list[schemas.TodoList])
async def getTodoList(db: Session = Depends(get_db)):
    return todoList.getAll(db)


@router.delete('/{code}')
async def deleteTodo(code:int, db:Session = Depends(get_db)):
    return todoList.delete(code, db)