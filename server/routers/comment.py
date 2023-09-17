from fastapi import APIRouter, HTTPException, status, Depends, Security
from sqlalchemy.orm.session import Session
from config.database import get_db
from config import db_comment
from schemas.comment import CommentBase, CommentDisplay
from schemas.token import TokenData
from config.db_auth import get_current_active_user
from typing import List

router = APIRouter(
    prefix='/comment',
    tags=['Comments']
)


@router.post('/', response_model=List[CommentDisplay], summary="Agrega un comentario a un post")
async def add_comment(resquest: CommentBase, db: Session = Depends(get_db), token: TokenData = Security(get_current_active_user, scopes=['post'])):
    """
    Agrega un comentario a un post existente

    - **username**: Nombre del creador del comentario
    - **text**: Texto del comentario
    - **post_id**: ID unico de post a comentar
"author_id": 0
    
    """
    db_comment.post_comment(db, resquest)
    lala = db_comment.get_all_comments(db, resquest.post_id)
    for resp in lala:
        if resp.responses:
            for resp2 in resp.responses:
                pass
    return lala


@router.get('/{post_id}', response_model=List[CommentDisplay])
async def get_comments(post_id: int, db: Session = Depends(get_db)):
    lala = db_comment.get_all_comments(db, post_id)
    for resp in lala:
        if resp.responses:
            for resp2 in resp.responses:
                pass
    return lala

@router.get('/onecomment/{comment_id}', response_model=CommentDisplay)
async def get_one_comment(comment_id: int, db:Session = Depends(get_db)):
    return db_comment.get_comment_by_id(db, comment_id)

@router.delete('/{comment_id}')
async def delete_comment(comment_id: int,  db:Session= Depends(get_db), token: TokenData = Security(get_current_active_user, scopes=['post'])):
    return db_comment.delete_selected_comment(db, comment_id, token.id)