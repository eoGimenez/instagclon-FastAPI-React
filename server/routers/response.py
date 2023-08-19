from fastapi import APIRouter, Depends, Security, HTTPException, status
from sqlalchemy.orm.session import Session
from config.database import get_db
from config import db_response
from schemas.response import ResponseBase
from schemas.token import TokenData
from config.db_auth import get_current_active_user

router = APIRouter(
    prefix='/response',
    tags=['Responses']
)

@router.get('/{comment_id}')
async def get_responses(comment_id: int, db:Session = Depends(get_db)):
    return db_response.get_all_responses(db, comment_id)

@router.post('/')
async def create_response(request: ResponseBase, db: Session = Depends(get_db), token: TokenData = Security(get_current_active_user, scopes=['post'])):
    if (request.author_id == token.id and request.username == token.username):
        return db_response.add_response(db, request)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                        detail='Se produjo un error en la Base de datos, intentelo nuevamente.')

@router.put('/{response_id}')
async def update_response(response_id: int, request: ResponseBase, db: Session = Depends(get_db), token: TokenData = Security(get_current_active_user, scopes=['post'])):
    if (request.author_id == token.id and request.username == token.username):
        return db_response.update_one_response(db, response_id, request)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                        detail='Se produjo un error en la Base de datos, intentelo nuevamente.')
@router.delete('/{response_id}')
async def delete_response(response_id: int, db: Session = Depends(get_db), token: TokenData = Security(get_current_active_user, scopes=['post'])):
    return db_response.delete_one_response(db, response_id, token.id)