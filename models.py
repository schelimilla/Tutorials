# what sqlalchemy (orm) uses to create tables we need in my sql database
# ddl - data definition language

from sqlalchemy import Boolean, Column, Integer, String
from database import Base 

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True) #first column in db, want to be able to index (faster performance)
    username = Column(String(50), unique=True) #instantiate string with varchar 50

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50))
    content = Column(String(100))
    user_id = Column(Integer) #foreign key