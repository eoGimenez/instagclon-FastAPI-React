from fastapi import APIRouter, Depends, HTTPException, status
from typing_extensions import Annotated
from datetime import timedelta
from schemas.user import UserBase, UserDisplay, UserSignUp
from schemas.token import Token
from config.database import get_db
from config import db_auth
from sqlalchemy.orm.session import Session
from fastapi.security import (
    OAuth2PasswordRequestForm
)
from config.db_user import post_user, get_user_by_id

ACCESS_TOKEN_EXPIRE_MINUTES = 30



router = APIRouter(
    tags=['Authentication']
)

@router.post('/signup', response_model=UserDisplay, summary="Crea un nuevo usuario")
async def create_user(request: UserSignUp, db: Session = Depends(get_db)):
    """
    Devolución de los datos del usuario a consumir en el front-end

    - **id**: ID unico del usuario
    - **username**: Nombre del usuario
    - **email**: Email del usuario
    - **avatar**: Al crear se le asigna un Avatar generico, luego puede actualizarse en el front-end
    """
    return post_user(db, request)

@router.get('/{id}', response_model=UserDisplay, summary="Devuelve busqueda de un Usuario por su ID")
async def get_user(id: int, db: Session = Depends(get_db)):
    """
    Devolución de los datos del usuario a consumir en el front-end

    - **id**: ID unico del usuario
    - **username**: Nombre del usuario
    - **email**: Email del usuario
    - **avatar**: Al crear se le asigna un Avatar generico, luego puede actualizarse en el front-end
    """
    return get_user_by_id(db, id)

@router.post('/token', response_model=Token, summary="Devuelve el token de autenticación")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    """
    Devolución del token de login

    - **access_token**: Token sifrado
    - **token_type**: Tipo de token
    - **User** = {
    
        - **id**: ID unico del usuario
        - **username**: Nombre del usuario
        - **email**: Email del usuario
        - **avatar**: Al crear se le asigna un Avatar generico, luego puede actualizarse en el front-end

    }
    """
    if (len(form_data.scopes) == 1):
        scopes = form_data.scopes[0].split(',')
    if (len(form_data.scopes) == 2):
        scopes = form_data.scopes
    user = db_auth.authenticate_user(
        form_data.username, form_data.password, db
    )
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid credentials')
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = db_auth.create_access_token(
        data={'sub': user.username, 'scopes': scopes, 'id': user.id},
        expires_delta=access_token_expires
    )
    return {
        'access_token': access_token,
        'token_type': 'bearer',
        'user': {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "avatar": user.avatar
        }
    }


@router.get("/users/me/", response_model=UserDisplay, summary="Comprueba validez del usuario")
async def read_users_me(
    current_user: Annotated[UserBase, Depends(db_auth.get_current_active_user)]
):
    """
    **¡¡REQUIERE ESTAR AUTENTICADO!!**

    Devolución de los datos del usuario a consumir en el front-end

    - **id**: ID unico del usuario
    - **username**: Nombre del usuario
    - **email**: Email del usuario
    - **avatar**: Al crear se le asigna un Avatar generico, luego puede actualizarse en el front-end
    """
    return current_user

@router.get("/status/", summary="Comprueba estado del usuario")
async def read_system_status(current_user: Annotated[UserBase, Depends(db_auth.get_current_user)]):
    """
    **¡¡REQUIERE ESTAR AUTENTICADO!!**

    Devolución completa del usuario

    - **status**: Tipo de estado del usuario
    - **Current user** = {
    
        - **id**: ID unico del usuario
        - **username**: Nombre del usuario
        - **email**: Email del usuario
        - **avatar**: Al crear se le asigna un Avatar generico, luego puede actualizarse en el front-end
        - **password**: Contraseña enctriptada
        - **active**: Estado de actividad del usuario

    }
    """
    return {
        "status": "ok",
        "current user": current_user
    }