import datetime
from database import Base
from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, String, Sequence
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'user'

    id_seq = Sequence('USER_ID_SEQ', metadata=Base.metadata, start=1)
    id = Column(Integer, id_seq, primary_key=True)
    email = Column(String(200), nullable=False, unique=True)
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(200), nullable=False)


class TodoList(Base):
    __tablename__ = "todolist"

    code_seq = Sequence('TODO_CODE_SEQ', metadata=Base.metadata, start=1)
    code = Column(Integer, code_seq, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)


class CheckList(Base):
    __tablename__ = "checklist"

    userid = Column(Integer, ForeignKey("user.id"), primary_key=True)
    code = Column(Integer, ForeignKey("todolist.code"), primary_key=True)
    done = Column(Boolean, default=False)
    date = Column(Date, default=datetime.datetime.utcnow, primary_key=True)