from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    username = Column(String)
    fullname = Column(String)
    created_at = Column(DateTime, server_default=func.now())

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String, nullable=False)
    description = Column(Text)
    due_date = Column(DateTime, nullable=False)
    is_completed = Column(Boolean, default=False)
    location = Column(String)
    created_at = Column(DateTime, server_default=func.now())

class AuthCode(Base):
    __tablename__ = 'auth_codes'
    id = Column(Integer, primary_key=True)
    phone = Column(String, index=True)
    code = Column(String)
    expires_at = Column(DateTime)
    is_used = Column(Boolean, default=False)
