from datetime import datetime, timedelta, timezone
from database import Base
from sqlalchemy import DATE, DATETIME, Boolean, Column, Date, DateTime, ForeignKey, Integer, String, Sequence, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class User(Base):
    __tablename__ = 'user'
    id_seq = Sequence('USER_ID_SEQ', metadata=Base.metadata, start=1)
    ROLE_USER, ROLE_COUNSELOR = 0, 1
    id = Column(Integer, id_seq, primary_key=True)
    email = Column(String(100), nullable=False, unique=True)
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    role = Column(Integer, default=ROLE_USER, nullable=False)
    profile = relationship("Profile", back_populates="user")
    participations = relationship('Participant', back_populates='user')
    messages = relationship('Message', back_populates='user')


class Profile(Base):
    __tablename__ = "profile"
    id_seq = Sequence('PROFILE_ID_SEQ', metadata=Base.metadata, start=1)
    id = Column(Integer, id_seq, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    path = Column(String(200), nullable=False)
    user = relationship('User', back_populates='profile')


class TodoList(Base):
    __tablename__ = "todolist"
    code_seq = Sequence('TODO_CODE_SEQ', metadata=Base.metadata, start=1)
    code = Column(Integer, code_seq, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)


class CheckList(Base):
    __tablename__ = "checklist"
    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    code = Column(Integer, ForeignKey("todolist.code"), primary_key=True)
    done = Column(Boolean, default=False)
    date = Column(DATE, default=func.now(), primary_key=True)


class Chatroom(Base):
    __tablename__ = 'chatroom'
    id_seq = Sequence("CHATROOM_ID_SEQ", metadata=Base.metadata, start=1)
    id = Column(Integer, id_seq, primary_key=True)
    messages = relationship('Message', back_populates='chatroom')
    participants = relationship('Participant', back_populates='chatroom')


class Message(Base):
    __tablename__ = 'message'
    id_seq = Sequence("MESSAGE_ID_SEQ", metadata=Base.metadata, start=1)
    id = Column(Integer, id_seq, primary_key=True)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    chatroom_id = Column(Integer, ForeignKey('chatroom.id'))
    timestamp = Column(
        DATETIME, default=datetime.utcnow, nullable=False)
    user = relationship('User', back_populates='messages')
    chatroom = relationship('Chatroom', back_populates='messages')


class Participant(Base):
    __tablename__ = 'participant'
    id_seq = Sequence("PARTICIPANT_ID_SEQ", metadata=Base.metadata, start=1)
    id = Column(Integer, id_seq, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    chatroom_id = Column(Integer, ForeignKey('chatroom.id'))
    last_read_message_id = Column(Integer, default=0)
    user = relationship('User', back_populates='participations')
    chatroom = relationship('Chatroom', back_populates='participants')
