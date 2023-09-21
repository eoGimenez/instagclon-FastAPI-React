import os
from sqlalchemy import create_engine
from fastapi import Depends
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import cloudinary
# from enviroment.config import Settings, get_settings

# dotenv : Settings = Depends(get_settings)

CLOUDNAME = os.environ.get('CLOUDNAME')
CLOUDKEY = os.environ.get('CLOUDKEY')
CLOUDSECRET = os.environ.get('CLOUDSECRET')

SQL_DB_URL = 'sqlite:///./instagram-db.db'

engine = create_engine(
    SQL_DB_URL,
    connect_args={'check_same_thread': False}
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)

cloudinary.config(
    cloud_name=CLOUDNAME,
    api_key=CLOUDKEY,
    api_secret=CLOUDSECRET
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()