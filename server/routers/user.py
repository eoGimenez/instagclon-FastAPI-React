from fastapi import APIRouter, Depends, HTTPException, status, Security
from schemas.user import UserDisplay
from schemas.token import Token
from config.database import get_db
from config import db_user
from config.db_auth import get_current_active_user
from sqlalchemy.orm.session import Session
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(
    prefix='/user',
    tags=['User'],
)

@router.put('/{user_id}', response_model=UserDisplay, summary="Actualizar datos del usuario")
async def update_user(user_id: int, request: UserDisplay, db: Session = Depends(get_db), token: Token = Security(get_current_active_user, scopes=['me'])):
    """
    **¡¡REQUIERE ESTAR AUTENTICADO!!**

    Actualiza datos del usuario

    - **id**: ID del usuario a editar
    - **username**: Nombre del usuario
    - **email**: Email del usuario
    - **avatar**: Imagen de perfil del usuario
    
    """
    return db_user.update_current_user(db, user_id, request)