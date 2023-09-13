from fastapi import APIRouter, Depends, Security, UploadFile, File
import cloudinary.uploader
import cloudinary
from sqlalchemy.orm.session import Session
from schemas.post import PostBase, PostDisplay
from config.database import get_db
from config import db_post
from schemas.token import TokenData
from config.db_auth import get_current_active_user
from typing import List

router = APIRouter(
    prefix='/post',
    tags=['Posts']
)


@router.post('/', response_model=PostDisplay)
async def create_post(request: PostBase, db: Session = Depends(get_db), token: TokenData = Security(get_current_active_user, scopes=['post'])):
    return db_post.post_post(db, request)


@router.get('/', response_model=List[PostDisplay])
async def get_posts(limit: int, db: Session = Depends(get_db)):
    return db_post.get_all_post(db, limit)


@router.post('/upload')
async def upload_file(image: UploadFile = File(...), token: TokenData = Security(get_current_active_user, scopes=['post'])):
    upload_result = cloudinary.uploader.upload(
        image.file, transformation={"width": 800, "height": 600})
    return {
        'public_id': upload_result['public_id'],
        'url': upload_result['secure_url']
    }


@router.get('/user_posts/{user_id}')
async def users_posts(user_id: int, db: Session = Depends(get_db)):
    return db_post.get_all_user_posts(db, user_id)


@router.get('/{id}', response_model=PostDisplay)
async def get_post(id: int, db: Session = Depends(get_db)):
    return db_post.get_post_by_id(db, id)


@router.delete('/{id}')
async def delete_post(id: int, db: Session = Depends(get_db), token: TokenData = Security(get_current_active_user, scopes=['post'])):
    return db_post.delete_post(db, id, token.id)
