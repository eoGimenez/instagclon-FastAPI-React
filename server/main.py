from fastapi import FastAPI
from models.models import Base
from config.database import engine

app = FastAPI()

@app.get('/')
def root():
    return "HEllo man"


Base.metadata.create_all(engine)