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
    Devuelve el post creado

    - **id**: ID unico del post
    - **image_url**: URL de la imagen del post
    - **caption**: Comentario del post
    - **timestamp**: Horario de creación del post
    - **author**: {
        - **id**: ID unico del usuario
        - **username**: Nombre del usuario
        - **avatar**: Al crear se le asigna un Avatar generico, luego puede actualizarse en el front-end
        - **actie**: Estado del usuario

            }
    - **comments**: [
        {
        - **id**: ID unico del comentario
        - **text**: Texto del comentario
        - **username**: Nombre del creador del comentario
        - **timestamp**: Horario de creacion del comentario
        - **responses**: [
            {
            - **id**: ID unico de la respuesta,
            - **text**: Texto de la respuesta
            - **username**: Nombre del creador de la respuesta
            - **edited**: Refleja si la respuesta fue editada,
            - **timestamp**: Horario de creacion de la respuesta
            - **author_response**: {
                - **id**: ID unico del usuario
                - **username**: Nombre del usuario
                - **avatar**: Al crear se le asigna un Avatar generico, luego puede actualizarse en el front-end
                - **actie**: Estado del usuario

                }

            }

        ]
        - **author_comment**: {
            - **id**: ID unico del usuario que creo el comentario
            - **username**: Nombre del usuario
            - **avatar**: Al crear se le asigna un Avatar generico, luego puede actualizarse en el front-end
            - **actie**: Estado del usuario

                }

        }

    ]

    """
    return db_post.post_post(db, request)


@router.get('/', response_model=List[PostDisplay])
async def get_posts(limit: int | None = 5, db: Session = Depends(get_db)):
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
