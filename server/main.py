import os
from fastapi import FastAPI
from routers import auth, post, comment, response, user
from models.models import Base
from config.database import engine
from fastapi.middleware.cors import CORSMiddleware
# from enviroment.config import Settings, get_settings


""" originis = [
    "http://localhost:3000",
    "http://localhost",
    "https://localhost:3000",
    "http://0.0.0.0:3000"
] """

# dotenv : Settings = get_settings()
ORIGIN = os.environ.get('ORIGIN')

app = FastAPI(
    title="API Red Social",
    description="""
    En esta API encontrarás los endpoints del ejercicio para simular una red social al estilo de Instagram.

    Ten en cuenta que utilizando el Swagger, los SCOPES pueden asignarse manualmente. 
    Cuando te autentiques, las últimas opciones son los SCOPES y para poder usar muchos 
    endpoints, debes utilizar los scopes correctos. 
    ESTAS OPCIONES ESTÁN HABILITADAS A MODO EDUCATIVO. 
    En el consumo de la API, está contemplada la asignación de SCOPES automáticamente.
    """,
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
    allow_origins= [ORIGIN],
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
