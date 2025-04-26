from sqlalchemy import Integer, String, Date, Column, ForeignKey, Boolean
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.sql.sqltypes import DateTime, Date
from datetime import datetime


class Base(DeclarativeBase):
    pass


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(180), nullable=False)
    phone = Column(String(80), nullable=False)
    birthday = Column(Date, nullable=False)
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"), default=None)
    user = relationship("User", backref="contacts")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    avatar = Column(String(255), nullable=True)
    confirmed = Column(Boolean, default=False, nullable=True)
