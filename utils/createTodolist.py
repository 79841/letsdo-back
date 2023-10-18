from repository import todoList
from sqlalchemy.orm import Session
from fastapi import Depends
import database


todo_data_set = [
    {"name": "휠체어에서  옷  갈아입기(하의,신발) 2회"},
    {"name": "트랜스퍼(침대,의자,소파,변기) 각2회"},
    {"name": "위생관리(머리감기, 샤워하기) 1회"},
    {"name": "스트레칭  5분"},
    {"name": "휠체어에서  엉덩이  들기  5회x3set"},
    {"name": "침대위에서  체위변경  5분x 2set"},
    {"name": "휠체어에서  엉덩이  들고  버티기  30초  이상"},
    {"name": "휠체어에서  바닦에  있는  물건  줍기  2회"},
    {"name": "휠체어  조작  연습(경사로, 단차) 5분"},
    {"name": "컴퓨터  자판  연습  10분  이상"},
]


get_db = database.get_db


def create_todolist():
    for todo_data in todo_data_set:
        for db in get_db():
            try:
                todoList.create(todo_data, db)
            except:
                ...


if __name__ == "__main__":
    create_todolist()
