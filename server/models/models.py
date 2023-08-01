from config.database import Base
from sqlalchemy.schema import ForeignKey
from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import String, Integer, Boolean, DateTime
from sqlalchemy.orm import relationship

class DbUser(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    active = Column(Boolean)
    items = relationship('DbPost', back_populates='author')

class DbPost(Base):
    __tablename__= 'posts'
    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String)
    caption = Column(String)
    timestamp = Column(DateTime)
    user_id = Column(Integer, ForeignKey('users.id'))
    author = relationship('DbUser', back_populates='items')