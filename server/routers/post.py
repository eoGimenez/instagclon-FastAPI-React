from fastapi import APIRouter, Depends, Security, UploadFile, File
from cloudinary.uploader import upload
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
async def get_posts(db: Session = Depends(get_db)):
    return db_post.get_all_post(db)

@router.post('/upload')
async def upload_file(image: UploadFile = File(...), token: TokenData = Security(get_current_active_user, scopes=['post'])):
    upload_result = upload(image.file)
    return {
        'public_id': upload_result['public_id'],
        'url': upload_result['secure_url']
    }

@router.delete('/{id}')
async def delete_post(id: int, db: Session = Depends(get_db), token: TokenData = Security(get_current_active_user, scopes=['post'])):
    return db_post.delete_post(db, id)