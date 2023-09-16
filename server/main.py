from fastapi import FastAPI
from routers import auth, post, comment, response, user
from models.models import Base
from config.database import engine
from fastapi.middleware.cors import CORSMiddleware


originis = [
    "http://localhost:3000",
    "http://localhost",
    "https://localhost:3000",
    "http://0.0.0.0:3000"
]


app = FastAPI(
    title="API Red Social",
    description="API creada a modo educativo",
    version="0.0.1",
    openapi_tags=[
        {
            "name": "Authentication",
            "description": "Rutas de autenticación"
        },
        {
            "name": "Posts",
            "description": "Rutas de Posts"
        },
        {
            "name": "Comments",
            "description": "Rutas de Comments"
        },
        {
            "name": "Responses",
            "description": "Rutas de Responses"
        },
        {
            "name": "User",
            "description": "Rutas de User"
        }
        ]
)

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
app.include_router(response.router)
app.include_router(user.router)


Base.metadata.create_all(engine)
