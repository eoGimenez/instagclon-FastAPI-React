from fastapi import FastAPI
from routers import auth, post, comment
from models.models import Base
from config.database import engine
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware import Middleware
# from starlette.middleware.cors import CORSMiddleware
# from enviroment.config import Settings, get_settings

# dotenv : Settings = get_settings()

originis = [
    "http://localhost:3000",
    "localhost:3000",
    "http://localhost",
    "https://localhost:3000"
]

middleware = [
    Middleware(
        CORSMiddleware,
    allow_origins= originis,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )
]

app = FastAPI(middleware=middleware)
print(originis)

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins= originis,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

app.include_router(auth.router)
app.include_router(post.router)
app.include_router(comment.router)


Base.metadata.create_all(engine)
