from sqlalchemy.orm.session import Session
from schemas.comment import CommentBase
from models.models import DbComment
from fastapi import HTTPException, status
from datetime import datetime

def post_comment(db: Session, request: CommentBase):
    new_comment = DbComment (
        text = request.text,
        username= request.username,
        post_id = request.post_id,
        user_id = request.author_id,
        edited = False,
        timestamp = datetime.now()
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

def get_all_comments(db: Session, post_id: int):
    return db.query(DbComment).filter(DbComment.post_id == post_id).all()

def get_comment_by_id(db: Session, id: int):
    return db.query(DbComment).filter(DbComment.id == id).first()

def update_one_comment(db: Session, id: int, request: CommentBase):
    response = db.query(DbComment).filter(DbComment.id == id)
    if not response.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Ese comentario no existe"
                            )

    response.update({
        DbComment.text: request.text,
        DbComment.edited: True
    })
    db.commit()
    return response.first()

def delete_selected_comment(db:Session, id: int, user_id: int):
    comment = db.query(DbComment).filter(DbComment.id == id).first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail='Esa respuesta no existe'
                            )
    if comment.author_comment.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Las respuestas solo pueden ser eliminadas por los creadores!'
        )
    db.delete(comment)
    db.commit()
    return 'Comentario eliminado'