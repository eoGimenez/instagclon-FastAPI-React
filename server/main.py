from fastapi import FastAPI
from routers import auth, post, comment
from models.models import Base
from config.database import engine
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    'http://localhost:3000'
]


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