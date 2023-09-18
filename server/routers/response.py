from fastapi import APIRouter, Depends, Security, HTTPException, status
from sqlalchemy.orm.session import Session
from config.database import get_db
from config import db_response
from schemas.response import ResponseBase, ResponseDisplay
from schemas.token import TokenData
from config.db_auth import get_current_active_user
from typing import List

router = APIRouter(
    prefix='/response',
    tags=['Responses']
)

@router.get('/{comment_id}', response_model=List[ResponseDisplay], summary="Devuelve las respuestas de un comentario")
async def get_responses(comment_id: int, db:Session = Depends(get_db)):
    """
    Devuelve un arreglo con todas las respuestas de un comentario

    - **comment_id**: ID del comentario a buscar

    """
    return db_response.get_all_responses(db, comment_id)

@router.post('/', response_model=ResponseDisplay, summary="Agrega una respuesta a un comentario")
async def create_response(request: ResponseBase, db: Session = Depends(get_db), token: TokenData = Security(get_current_active_user, scopes=['post'])):
    """
    **¡¡REQUIERE ESTAR AUTENTICADO Y SER EL AUTOR DEL COMENTARIO!!**

    Agrega una respuesta a un comentario


    
    """
    if (request.author_id == token.id and request.username == token.username):
        return db_response.add_response(db, request)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                        detail='Se produjo un error en la Base de datos, intentelo nuevamente.')

@router.put('/{response_id}', response_model=ResponseDisplay)
async def update_response(response_id: int, request: ResponseBase, db: Session = Depends(get_db), token: TokenData = Security(get_current_active_user, scopes=['post'])):
    if (request.author_id == token.id and request.username == token.username):
        return db_response.update_one_response(db, response_id, request)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                        detail='Se produjo un error en la Base de datos, intentelo nuevamente.')
@router.delete('/{response_id}')
async def delete_response(response_id: int, db: Session = Depends(get_db), token: TokenData = Security(get_current_active_user, scopes=['post'])):
    return db_response.delete_one_response(db, response_id, token.id)