from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import cloudinary
from enviroment.config import Settings, get_settings

dotenv : Settings = get_settings()

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
    cloud_name=dotenv.cloudname,
    api_key=dotenv.cloudkey,
    api_secret=dotenv.cloudsecret
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()