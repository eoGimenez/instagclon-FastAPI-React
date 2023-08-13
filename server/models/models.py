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
    avatar = Column(String)
    items = relationship('DbPost', back_populates='author')

class DbPost(Base):
    __tablename__= 'posts'
    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String)
    caption = Column(String)
    timestamp = Column(DateTime)
    user_id = Column(Integer, ForeignKey('users.id'))
    author = relationship('DbUser', back_populates='items')
    comments = relationship('DbComment', back_populates='post')

class DbComment(Base):
    __tablename__= 'comments'
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    username = Column(String)
    timestamp = Column(DateTime)
    post_id = Column(Integer, ForeignKey('posts.id'))
    post = relationship('DbPost', back_populates='comments')
    responses = relationship('DbResponse', back_populates='comment')

class DbResponse(Base):
    __tablename__= 'responses'
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    username = Column(String)
    edited = Column(Boolean)
    timestamp = Column(DateTime)
    comment_id = Column(Integer, ForeignKey('comments.id'))
    comment = relationship('DbComment', back_populates='responses')