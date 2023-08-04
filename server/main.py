from fastapi import FastAPI
from routers import auth, post, comment
from models.models import Base
from config.database import engine
from fastapi.middleware.cors import CORSMiddleware


originis = [
    "http://localhost:3000",
    "http://localhost",
    "https://localhost:3000",
    "http://0.0.0.0:3000"
]


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins= originis,
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'PUT', 'DELETE'],
    allow_headers=["*"],
    expose_headers=["*"],
)

app.include_router(auth.router)
app.include_router(post.router)
app.include_router(comment.router)


Base.metadata.create_all(engine)
