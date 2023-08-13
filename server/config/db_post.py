from sqlalchemy.orm.session import Session
from schemas.post import PostBase
from models.models import DbPost
from fastapi import HTTPException, status
from datetime import datetime

def post_post(db: Session, request: PostBase):
    new_post = DbPost(
        image_url = request.image_url,
        caption = request.caption,
        timestamp = datetime.now(),
        user_id = request.author_id 
     )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

def get_all_post(db: Session):
    return db.query(DbPost).all()

def get_post_by_id(db: Session, id:int):
    return db.query(DbPost).filter(DbPost.id == id).first()

def delete_post(db: Session, id: int, user_id: int):
    post = db.query(DbPost).filter(DbPost.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No pudimos encontrar el post con id: {id}, intentelo nuevamente. ')
    if post.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Solo puedes borrar post de los que seas propietario.')
    db.delete(post)
    db.commit()
    return 'El post fue eliminado correctamente.'