from fastapi import FastAPI
from routers import auth, post, comment
from models.models import Base
from config.database import engine
from fastapi.middleware.cors import CORSMiddleware
from enviroment.config import Settings, get_settings

dotenv : Settings = get_settings()

app = FastAPI()


app.include_router(auth.router)
app.include_router(post.router)
app.include_router(comment.router)


Base.metadata.create_all(engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins= [dotenv.ORIGIN],
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*'],
)