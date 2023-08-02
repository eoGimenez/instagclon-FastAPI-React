from fastapi import APIRouter, HTTPException, status, Depends, Security
from sqlalchemy.orm.session import Session
from config.database import get_db
from config import db_comment
from schemas.comment import CommentBase, CommentDisplay
from schemas.token import TokenData
from config.db_auth import get_current_active_user

router = APIRouter(
    prefix='/comment',
    tags=['Comments']
)


@router.post('/')
async def add_comment(resquest: CommentBase, db: Session = Depends(get_db), token: TokenData = Security(get_current_active_user, scopes=['post'])):
    return db_comment.post_comment(db, resquest)


@router.get('/{post_id}')
async def get_comments(post_id: int, db: Session = Depends(get_db)):
    return db_comment.get_all_comments(db, post_id)