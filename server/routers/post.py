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


@router.post('/', response_model=PostDisplay,summary="Crea nuevo Post")
async def create_post(request: PostBase, db: Session = Depends(get_db), token: TokenData = Security(get_current_active_user, scopes=['post'])):
    """
    **¡¡REQUIERE ESTAR AUTENTICADO!!**

    Crea un nuevo post

    - **image_url**: URL de la imagen del post
    - **caption**: Comentario del post
    - **author_id**: ID del user creador del post 
    """
    return db_post.post_post(db, request)


@router.get('/', response_model=List[PostDisplay], summary="Devuelve todos los posts")
async def get_posts(limit: int, db: Session = Depends(get_db)):
    """
    Devuelve un arreglo con posts
    
    - **limit**: Ingresar el número de posts a devolver
    
    """

    return db_post.get_all_post(db, limit)


@router.post('/upload', summary="Sube una imagen a la db")
async def upload_file(image: UploadFile = File(...), token: TokenData = Security(get_current_active_user, scopes=['post'])):
    """
    **¡¡REQUIERE ESTAR AUTENTICADO!!**

    Gestiona la imagen para subirla a la base de datos

    - **Opcion de selección de imagen**

    """
    upload_result = cloudinary.uploader.upload(
        image.file, transformation={"width": 800, "height": 600})
    return {
        'public_id': upload_result['public_id'],
        'url': upload_result['secure_url']
    }


@router.get('/user_posts/{user_id}', response_model=List[PostDisplay], summary="Devuelve todos los posts de un usuario")
async def users_posts(user_id: int, db: Session = Depends(get_db)):
    """
    Devuelve un arreglo con todos los post que tenga un usuario
    
    - **user_id**: ID del autor de los posts a buscar

    """
    return db_post.get_all_user_posts(db, user_id)


@router.get('/{post_id}', response_model=PostDisplay, summary="Devuelve el post por ID")
async def get_post(post_id: int, db: Session = Depends(get_db)):
    """
    Devuelve un post

    - **post_id**: Devuelve el post por su ID unico
    """
    return db_post.get_post_by_id(db, post_id)


@router.delete('/{id}', summary="Elimina el post por ID")
async def delete_post(id: int, db: Session = Depends(get_db), token: TokenData = Security(get_current_active_user, scopes=['post'])):
    """
    Elimina el post por ID

    - **Confirmación de eliminación**

    """
    return db_post.delete_post(db, id, token.id)
