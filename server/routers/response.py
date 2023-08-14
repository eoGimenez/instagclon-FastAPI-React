from fastapi import APIRouter, Depends, Security
from sqlalchemy.orm.session import Session
from config.database import get_db
from config import db_response
from schemas.response import ResponseDisplay, ResponseBase
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
    return db_response.add_response(db, request)