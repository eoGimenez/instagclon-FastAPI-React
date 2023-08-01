from fastapi import FastAPI, Depends
from typing_extensions import Annotated
from routers import auth, post
from models.models import Base
from config.database import engine
from enviroment.config import Settings, get_settings

app = FastAPI()


@app.get('/')
def root(settings: Annotated[Settings, Depends(get_settings)]):
    return settings

app.include_router(auth.router)
app.include_router(post.router)

Base.metadata.create_all(engine)