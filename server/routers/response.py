from fastapi import APIRouter, Depends, Security, HTTPException, status
from sqlalchemy.orm.session import Session
from config.database import get_db
from config import db_response
from schemas.response import ResponseBase, ResponseDisplay, ResponsePost
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

@router.post('/{comment_id}', response_model=ResponseDisplay, summary="Agrega una respuesta a un comentario")
async def create_response(comment_id: int, request: ResponsePost, db: Session = Depends(get_db), token: TokenData = Security(get_current_active_user, scopes=['post'])):
    """
    **¡¡REQUIERE ESTAR AUTENTICADO Y SER EL AUTOR DE LA RESPUESTA!!**

    Agrega una respuesta a un comentario

    - **comment_id**: ID del comentario a responder
    - **username**: Nombre del creador de la respuesta
    - **text**: Texto de la respuesta
    - **author_id**: ID unico del autor de la respuesta
    
    """
    if (request.author_id == token.id and request.username == token.username):
        return db_response.add_response(db, comment_id, request)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                        detail='Se produjo un error en la Base de datos, intentelo nuevamente.')

@router.put('/{response_id}', response_model=ResponseDisplay, summary="Edita una respuesta")
async def update_response(response_id: int, request: ResponseBase, db: Session = Depends(get_db), token: TokenData = Security(get_current_active_user, scopes=['post'])):
    """
    **¡¡REQUIERE ESTAR AUTENTICADO Y SER EL AUTOR DE LA RESPUESTA!!**

    Edita una respuesta siendo el autor

    - **response_id**: ID de la respuesta a editar
    - **comment_id**: ID del comentario a responder
    - **username**: Nombre del creador de la respuesta
    - **text**: Texto de la respuesta
    - **author_id**: ID unico del autor de la respuesta
    
    """
    if (request.author_id == token.id and request.username == token.username):
        return db_response.update_one_response(db, response_id, request)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                        detail='Se produjo un error en la Base de datos, intentelo nuevamente.')
@router.delete('/{response_id}', summary="Elimina una respuesta por su ID")
async def delete_response(response_id: int, db: Session = Depends(get_db), token: TokenData = Security(get_current_active_user, scopes=['post'])):
    """
    **¡¡REQUIERE ESTAR AUTENTICADO Y SER EL AUTOR DE LA RESPUESTA!!**

    Elimina la respuesta siendo el autor.

    - **response_id**: ID de la respuesta a eliminar

    """
    return db_response.delete_one_response(db, response_id, token.id)