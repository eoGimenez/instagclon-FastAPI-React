from sqlalchemy.orm.session import Session
from schemas.comment import CommentBase
from models.models import DbComment
from fastapi import HTTPException, status
from datetime import datetime

def post_comment(db: Session, request: CommentBase):
    new_comment = DbComment (
        text = request.text,
        username= request.username,
        timestamp = datetime.now(),
        post_id = request.post_id
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

def get_all_comments(db: Session, post_id: int):
    return db.query(DbComment).filter(DbComment.post_id == post_id)