from fastapi import FastAPI, Depends
from typing_extensions import Annotated
from routers import auth
from models.models import Base
from config.database import engine
from enviroment import config_env, envirom

app = FastAPI()


@app.get('/')
def root(settings: Annotated[config_env.Settings, Depends(envirom.get_settings)]):
    return settings

app.include_router(auth.router)

Base.metadata.create_all(engine)