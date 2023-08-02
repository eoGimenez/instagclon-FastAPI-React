from fastapi import FastAPI, Depends
from typing_extensions import Annotated
from routers import auth, post, comment
from models.models import Base
from config.database import engine
from enviroment.config import Settings, get_settings
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    'http://localhost:3000'
]

@app.get('/')
def root(settings: Annotated[Settings, Depends(get_settings)]):
    return settings

app.include_router(auth.router)
app.include_router(post.router)
app.include_router(comment.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*'],
)

Base.metadata.create_all(engine)