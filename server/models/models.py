from config.database import Base
from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import String, Integer, Boolean

class DbUser(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    active = Column(Boolean)