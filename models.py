import datetime
from database import Base
from sqlalchemy import DATE, DATETIME, Boolean, Column, Date, DateTime, ForeignKey, Integer, String, Sequence, Text
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'user'

    id_seq = Sequence('USER_ID_SEQ', metadata=Base.metadata, start=1)
    ROLE_USER, ROLE_COUNSELOR = 0, 1
    id = Column(Integer, id_seq, primary_key=True)
    email = Column(String(200), nullable=False, unique=True)
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(200), nullable=False)
    role = Column(int, default=ROLE_USER, nullable=False)


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
    date = Column(DATE, default=datetime.datetime.utcnow, primary_key=True)


class Message(Base):
    __tablename__ = "message"

    id_seq = Sequence('MESSAGE_ID_SEQ', metadata=Base.metadata, start=1)
    message_id = Column(Integer, id_seq, primary_key = True)
    message_from = Column(String(100), nullable=False)
    message_to = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DATETIME, default=datetime.datetime.utcnow, nullable=False)

class Chatroom(Base):
    __tablename__ = "chatroom"






